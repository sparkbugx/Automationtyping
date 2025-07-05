# Automationtyping
MonkeyType Automation Script

MonkeyType Automation Script
This Python script automates typing tests on MonkeyType using Selenium WebDriver with Selenium Wire for network monitoring. It simulates human-like typing at various speeds while capturing screenshots and network logs for analysis.
![image](https://github.com/user-attachments/assets/9087b034-d79d-4d68-9342-1d17b0402e62)

Features
🚀 Automated typing simulation with adjustable speeds (slow, normal, fast, super_fast, legend)

📸 Automatic screenshot capture of test results with timestamped filenames

🧞 Network traffic logging with response bodies for analysis

⏱️ Precise timing control for typing duration and pauses

🍪 Cookie consent handling (automatically rejects cookies)

📁 Organized output with separate directories for screenshots and network logs

🛡️ Error handling with automatic failure documentation

Usage
Install required packages:

bash
pip install selenium selenium-wire
Run the script:

python
python monkeytype_automation.py
Customize typing speed by modifying the speed parameter:

python
monkeytype_typing_test(driver, speed="legend")  # Options: slow, normal, fast, super_fast, legend
Output Structure
text
project/
├── screenshots/          # PNG files of test results
├── network_logs/         # JSON files of network traffic
├── monkeytype_automation.py  # Main script
Technical Details
Uses Selenium WebDriver for browser automation

Implements Selenium Wire for network traffic interception

Includes intelligent waiting mechanisms with WebDriverWait

Features text cleaning for proper JSON serialization

Simulates human typing patterns with variable delays

Use Cases
Performance testing of typing applications

Benchmarking different typing speeds

Automated testing of web-based typing platforms

Network traffic analysis of real-time applications

📋 Requirements
Python Packages
Install the required packages using pip:
![image](https://github.com/user-attachments/assets/79865239-4347-465b-868e-1f3220aafc15)

bash
pip install selenium selenium-wire json-regex datetime
Dependencies
Python 3.6+

Selenium (selenium) – For browser automation

Selenium-Wire (selenium-wire) – For network traffic interception

ChromeDriver – Must match your installed Chrome version

Google Chrome – Browser for automation

Optional (for development/testing)
pytest (for running tests)

black (code formatting)

Installation Steps
Install Python packages:

bash
pip install -r requirements.txt
(If you create a requirements.txt file with the listed packages.)

Download ChromeDriver:

Get the correct version from ChromeDriver Downloads.

Ensure it's in your PATH or specify its location in the script.

Run the script:

bash
python monkeytype_automation.py






Selenium Version used on this proyect
selenium>=4.0.0
selenium-wire>=5.1.0


