#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LinkConan(ConanFile):
	name = "link"
	version = "1.0.0"
	url = "https://github.com/Ableton/link"
	description = "A technology that synchronizes musical beat, tempo, and phase across multiple applications running on one or more devices"
	license = "GPLv2+"
	exports = ["LICENSE.md"]

	settings = "os"
	
	exports_sources = ["CMakeLists.txt"]
	generators = "cmake"

	source_subfolder = "source_subfolder"

	def source(self):
		self.run("git clone --branch Link-1.0.0 --depth 1 --quiet https://github.com/Ableton/link.git ")
		self.run("cd link && git submodule update --init modules/asio-standalone")
		self.run("cd ..")
		os.rename("link", self.source_subfolder)


	def package(self):
		self.copy(pattern="LICENSE.md", src=self.source_subfolder)
		include_folder = os.path.join(self.source_subfolder, "include")
		self.copy(pattern="*.hpp", dst="include", src=include_folder)
		self.copy(pattern="*.ipp", dst="include", src=include_folder)
		
		asio_source_folder = os.path.join(self.source_subfolder, "modules", "asio-standalone", "asio")
		self.copy(pattern="LICENSE_1_0.txt", dst="modules/asio-standalone", src=asio_source_folder)
		asio_include_folder = os.path.join(asio_source_folder, "include")
		self.copy(pattern="*.hpp", dst="modules/asio-standalone/include", src=asio_include_folder)
		self.copy(pattern="*.ipp", dst="modules/asio-standalone/include", src=asio_include_folder)


	def package_info(self):
		self.info.header_only()
		
		self.cpp_info.includedirs = [ "include", "modules/asio-standalone/include" ]
		
		if self.settings.os == "Windows":
			platform_define = "LINK_PLATFORM_WINDOWS=1"
		elif self.settings.os == "Macos":
			platform_define = "LINK_PLATFORM_MACOSX=1"
		else:
			platform_define = "LINK_PLATFORM_LINUX=1"
		
		self.cpp_info.defines = [ platform_define ]
