from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = REPO_ROOT / "scripts" / "macos" / "start_bosshunter.sh"
INSTALLER = REPO_ROOT / "scripts" / "macos" / "install_launcher.command"


class MacOSLauncherTests(unittest.TestCase):
	def test_launcher_is_portable_and_opens_both_services(self):
		text = LAUNCHER.read_text(encoding="utf-8")
		self.assertIn("#!/bin/bash", text)
		self.assertIn("BASH_SOURCE", text)
		self.assertIn("bosshunter.main", text)
		self.assertIn("--python-path", text)
		self.assertIn("command -v bosshunter", text)
		self.assertIn("remote-debugging-port=9222", text)
		self.assertIn("--user-data-dir", text)
		self.assertIn("http://127.0.0.1:8686", text)
		self.assertIn("web --no-open", text)
		# Dedicated profile is mandatory: Chrome 136+ blocks debug ports on it.
		self.assertIn(".bosshunter-chrome", text)
		self.assertNotIn("/Users/pikachu", text)

	def test_installer_creates_a_double_click_entry(self):
		text = INSTALLER.read_text(encoding="utf-8")
		self.assertIn("#!/bin/bash", text)
		self.assertIn("BASH_SOURCE", text)
		self.assertIn("start_bosshunter.sh", text)
		self.assertIn("$HOME/Desktop", text)
		self.assertIn("BossHunter.command", text)
		self.assertIn("chmod +x", text)
		self.assertNotIn("/Users/pikachu", text)

	def test_launcher_scripts_are_executable(self):
		for script in (LAUNCHER, INSTALLER):
			mode = script.stat().st_mode
			self.assertTrue(mode & 0o100, f"{script.name} is not executable")


if __name__ == "__main__":
	unittest.main()
