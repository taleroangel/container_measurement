#include "opencv2/core/mat.hpp"
#include <cassert>
#include <cstddef>
#include <cstdio>
#include <cstdlib>

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

/* --------- Main function --------- */
int main(int argc, char *argv[]) {

  // Vallidate parameters
  std::string input_file;
  std::string output_file;
  std::string kernel_path;
  bool use_grayscale = false;
  int do_times = 1;

  auto cli = (
      // Input directory
      ((clipp::required("-i", "--input") &
        clipp::value("input_file", input_file)) %
       "Input file to process"),

      // Output file extension
      ((clipp::required("-o", "--output") &
        clipp::value("output_file", output_file)) %
       "Output file name"),

      // Output file extension
      ((clipp::required("-k", "--kernel") &
        clipp::value("kernel_file", kernel_path)) %
       "Convolution kernel file (.kernel)"),

      // Use grayscale
      (clipp::option("-g", "--grayscale").set(use_grayscale) %
       "Transform to grayscale before processing"),

      // Repeat transformation
      ((clipp::option("-t", "--times") &
        clipp::opt_integer("n_times=1", do_times)) %
       "Do the convolution n times (1 by default)"));

  if (!clipp::parse(argc, argv, cli)) {
    std::cerr << std::flush;
    fmt::print(stderr, fmt::bg(fmt::color::red), "Invalid Usage!");
    std::cerr << std::endl
              << clipp::make_man_page(cli, argv[0])
                     .prepend_section("DESCRIPTION",
                                      "Apply a convolution kernel to an image")
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
        "\nApply a convolution kernel to an image\n");
  }

  // Show parameters
  fmt::print(fmt::fg(fmt::color::purple), "\nInput File: '{}'\n", input_file);
  fmt::print(fmt::fg(fmt::color::purple), "Output File: '{}'\n", output_file);

  // Show OpenCV version
  fmt::print(fmt::fg(fmt::color::blue_violet), "\nUsing OpenCV version: {}\n",
             CV_VERSION);

  // Show additional information
  fmt::print(fmt::fg(fmt::color::blue), "Grayscale: {}\n", use_grayscale);
  fmt::print(fmt::fg(fmt::color::blue), "Additional Repeats: {}\n", do_times);

  // Read the kernel
  cv::Mat kernel;
  try {
    // Print information about the kernel
    fmt::print(fmt::fg(fmt::color::blue_violet), "Using Kernel: {}\n",
               kernel_path);
    kernel = read_kernel(kernel_path);
    // Print the kernel
    std::cout << kernel << std::endl;
  } catch (...) {
    fflush(stdout);
    fmt::print(stderr, fmt::bg(fmt::color::red), "[{}]", "Kernel file failure");
    fmt::print(stderr, fmt::fg(fmt::color::red),
               "\tUnable to load kernel file\n");
    return EXIT_FAILURE;
  }

  // Initialize
  fmt::print(fmt::fg(fmt::color::navy), "\nApplying convolutions to image\n");
  // Read image
  fmt::print(fmt::fg(fmt::color::yellow), "[{}]\t", input_file);
  fflush(stdout);

  // Import image matrix OpenCV
  cv::Mat image = cv::imread(input_file, use_grayscale ? cv::IMREAD_GRAYSCALE
                                                       : cv::IMREAD_COLOR);

  try {
    // Repeat convolution do_times
    for (int it = 0; it < do_times; it++) {
      // Show a processing indicator
      std::cout << ". " << std::flush;
      // Repeat the convolution
      image = convolute_image(image, kernel);
    }

    // Write image
    fmt::print("\t{} ", output_file);
    fflush(stdout);
    cv::imwrite(output_file, image);

    // Finalize
    fmt::print(fmt::bg(fmt::color::green), "OK");
  } catch (const cv::Exception &e) {
    // Show an OpenCV Exception
    fmt::print(fmt::bg(fmt::color::red), "\tOpenCVException");
    fmt::print(fmt::fg(fmt::color::red), "\t{}\t", e.what());
  } catch (...) {
    // Show generic exception
    fmt::print(fmt::bg(fmt::color::red), "\tUnknownException");
  }

  std::cout << std::endl;
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
