# Instagram Downloader

## Description
This Python project is an Instagram downloader built using Selenium. It allows users to download saved posts or the entire profile of an Instagram account to their PC desktop.

## Requirements
- Python 3.x
- Selenium
- geckodriver (for Firefox)
  
## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_username/instagram-downloader.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd instagram-downloader
   ```
3. **Install the required dependencies**:
   ```bash
   pip install selenium
   ```

## Usage
1. Make sure you have installed Firefox browser on your system.
2. **Download geckodriver** from [here](https://github.com/mozilla/geckodriver/releases) and place it in your system's PATH (Meaning the same directory where the project files are).
3. **Run the script**:
   ```bash
   python Main.py
   ```
4. Follow the prompts to sign in to your Instagram account.
5. Choose what information to download:
   - Enter **1** to download the entire profile.
   - Enter **2** to download saved posts.
   - Enter **3** to quit.
6. Sit back and relax while the script downloads the Instagram posts.
7. Program will terminate with an error if network issues are encountered. Posts failed to download will try again when all the initial posts are attempted.

## Disclaimer
This project is for educational purposes only. It is your responsibility to use this tool in compliance with Instagram's terms of service and copyright laws.

## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the **MIT License**. See the LICENSE file for details.
