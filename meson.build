project('cloud_image_processing', 'cpp',
  version : '0.1',
  default_options : [
		'auto_features=disabled',
  		'warning_level=0',
    	'cpp_std=c++17',
		'debug=false',
		'buildtype=release',
		'optimization=3',
	])

# Dependencies
dependencies = [
	dependency('opencv4'),
	dependency('fmt'),
	dependency('clipp'),
]

exe = executable(
		'apply_convolution',
		files('./src/main.cpp'),
		dependencies: dependencies
	)
