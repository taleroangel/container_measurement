#include <cassert>
#include <cstddef>
#include <cstdio>
#include <cstdlib>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <ostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include <clipp.h>
#include <fmt/color.h>
#include <fmt/core.h>
#include <fmt/format.h>
#include <opencv2/opencv.hpp>

/* --------- Function declarations --------- */
cv::Mat read_kernel(std::string path);
cv::Mat convolute_image(cv::Mat image, cv::Mat kernel);
std::vector<std::string> find_files_in_directory(std::filesystem::path,
                                                 std::string filter);

/* --------- Main function --------- */
int main(int argc, char *argv[]) {

  // Vallidate parameters
  std::string input_directory;
  std::string input_extension;
  std::string output_extension;
  std::string kernel_path;
  bool use_grayscale = false;
  int repeat = 0;

  auto cli = (
      // Input directory
      ((clipp::required("-i", "--input") &
        clipp::value("input_directory", input_directory)) %
       "Input directory from which the files will be grabbed"),

      // File extension
      ((clipp::required("-e", "--extension") &
        clipp::value("extension_filter", input_extension)) %
       "File extension filtering"),

      // Output file extension
      ((clipp::required("-o", "--output") &
        clipp::value("output_extension", output_extension)) %
       "Result file extension"),

      // Output file extension
      ((clipp::required("-k", "--kernel") &
        clipp::value("kernel_file", kernel_path)) %
       "Convolution kernel file"),

      // Use grayscale
      (clipp::option("-g", "--grayscale").set(use_grayscale) %
       "Transform to grayscale"),

      // Repeat transformation
      ((clipp::option("-r", "--repeat") &
        clipp::opt_integer("n_times=0", repeat)) %
       "Repeat the transformation n times (0 by default)"));

  if (!clipp::parse(argc, argv, cli)) {
    std::cerr << std::flush;
    fmt::print(stderr, fmt::bg(fmt::color::red), "Invalid Usage!");
    std::cerr << std::endl
              << clipp::make_man_page(cli, argv[0])
                     .prepend_section("DESCRIPTION",
                                      "Apply a convolution kernel to a group "
                                      "of images in a directory")
                     .prepend_section(
                         "CREDITS",
                         "Angel D. Talero (angelgotalero@outlook.com) under "
                         "MIT Licence\nFind me on GitHub as @taleroangel");
    return EXIT_FAILURE;
  } else {
    // Show a welcome message
    fmt::print(fmt::bg(fmt::color::indigo) | fmt::emphasis::bold,
               "ApplyConvolution - @taleroangel");
    fmt::print(
        fmt::fg(fmt::color::indigo) | fmt::emphasis::italic,
        "\nApply a convolution kernel to multiple images in a directory\n");
  }

  // Obtain parameters
  fmt::print(fmt::fg(fmt::color::purple), "\nCurrent Directory: '{}'\n",
             input_directory);
  fmt::print(fmt::fg(fmt::color::purple), "File Extension: '{}'\n",
             input_extension);

  std::vector<std::string> files;

  try {
    // Obtain files from filesystem
    files = find_files_in_directory(input_directory, input_extension);
  } catch (const std::filesystem::filesystem_error &e) {
    fflush(stdout);
    fmt::print(stderr, fmt::bg(fmt::color::red), "[{}]",
               "Failed to load directory");
    fmt::print(stderr, fmt::fg(fmt::color::red), "\t{}\n", e.what());
    return EXIT_FAILURE;
  }

  // Show files in filesystem
  for (const auto &file : files) {
    fmt::print(fmt::emphasis::italic, "\t{}\n", file);
  }

  // Show OpenCV version
  fmt::print(fmt::fg(fmt::color::blue_violet), "\nUsing OpenCV version: {}\n",
             CV_VERSION);

  // Show additional information
  fmt::print(fmt::fg(fmt::color::blue), "Grayscale: {}\n", use_grayscale);
  fmt::print(fmt::fg(fmt::color::blue), "Additional Repeats: {}\n", repeat);

  // Read the kernel
  cv::Mat kernel;
  try {
    // Print information about the kernel
    fmt::print(fmt::fg(fmt::color::blue_violet), "Using Kernel: {}\n",
               kernel_path);
    kernel = read_kernel(kernel_path);
    std::cout << kernel << std::endl;
  } catch (...) {
    fflush(stdout);
    fmt::print(stderr, fmt::bg(fmt::color::red), "[{}]", "Kernel file failure");
    fmt::print(stderr, fmt::fg(fmt::color::red),
               "\tUnable to load kernel file\n");
    return EXIT_FAILURE;
  }

  // Process every image
  fmt::print(fmt::fg(fmt::color::medium_blue), "\nImage processing:\n");
  for (const auto &file : files) {
    // Read image
    fmt::print(fmt::fg(fmt::color::yellow), "{}\t", file);
    fflush(stdout);
    cv::Mat image = cv::imread(file, use_grayscale ? cv::IMREAD_GRAYSCALE
                                                   : cv::IMREAD_COLOR);

    try {
      // Calculate convolution
      auto result = convolute_image(image, kernel);

      // Additional iterations
      for (int it = 0; it < repeat; it++) {
        std::cout << ". " << std::flush;
        result = convolute_image(result, kernel);
      }

      // Calculate output filename
      std::string result_filename{file};
      result_filename.replace(file.find(input_extension),
                              input_extension.length(), output_extension.data(),
                              output_extension.length());

      // Write image
      fmt::print("{}\t", result_filename);
      fflush(stdout);
      cv::imwrite(result_filename, result);

      // Finalize
      fmt::print(fmt::bg(fmt::color::green), "OK");
    } catch (const cv::Exception &e) {
      // Show an OpenCV Exception
      fmt::print(fmt::bg(fmt::color::red), "OpenCVException");
      fmt::print(fmt::fg(fmt::color::red), "\t{}\t", e.what());
    } catch (...) {
      // Show generic exception
      fmt::print(fmt::bg(fmt::color::red), "UnknownException");
    }

    std::cout << std::endl;
  }

  fmt::print(fmt::fg(fmt::color::green), "\nFinished procedure!\n");
  return EXIT_SUCCESS;
}

/* --------- Function definitions --------- */

cv::Mat read_kernel(std::string path) {
  // Store file values
  std::vector<std::vector<float>> matrix;

  // Read the kernel file
  if (std::ifstream kernel_file{path, std::ios::in}) {

    // Read all lines in file
    std::string line;
    while (std::getline(kernel_file, line)) {
      // Rows
      std::vector<float> row;
      std::istringstream iss{line};

      // Read every value of line
      float value;
      while (iss >> value) {
        row.push_back(value);
      }

      // Push row into matrix
      matrix.push_back(row);
    }
    // Create the kernel
  } else {
    throw std::runtime_error("Unable to parse file");
  }

  // Create the kernel
  cv::Mat kernel(matrix.size(), matrix[0].size(), CV_32F);

  // Asign values to kernel
  for (size_t ii = 0; ii < matrix.size(); ii++) {
    for (size_t jj = 0; jj < matrix[ii].size(); jj++) {
      // Ensure all rows are same size
      assert(matrix[ii].size() == matrix[0].size());
      // Append it to kernel
      kernel.at<float>(ii, jj) = matrix[ii][jj];
    }
  }

  return kernel;
}

std::vector<std::string> find_files_in_directory(std::filesystem::path path,
                                                 std::string filter) {
  std::vector<std::string> entries;
  for (const auto &entry : std::filesystem::directory_iterator(path)) {
    if (entry.is_regular_file() &&
        (entry.path().native().find(filter) != std::string::npos)) {
      entries.push_back(entry.path());
    }
  }

  return entries;
}

cv::Mat convolute_image(cv::Mat image, cv::Mat kernel) {
  // Check if image is empty
  if (image.empty()) {
    throw std::runtime_error("Invalid image");
  }

  // Result matrix
  cv::Mat result;
  // Create convolution
  cv::filter2D(image, result, CV_32F, kernel);

  return result;
}
