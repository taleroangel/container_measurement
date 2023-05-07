from conan import ConanFile
from conan.tools.meson import Meson


class CloudImageProcessingRecipe(ConanFile):

    # Metadata
    name = "cloud_image_processing"
    version = "1.0"
    license = "MIT"

    author = "Angel Talero (angelgotalero@outlook.com)"
    description = """Cloud container measurement example"""

    # Configuration
    settings = "os", "arch", "compiler", "build_type"
    generators = "PkgConfigDeps", "MesonToolchain"

    requires = ["clipp/1.2.3"]

    def build(self):
        meson = Meson(self)
        meson.configure()
        meson.build()

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = "build"
