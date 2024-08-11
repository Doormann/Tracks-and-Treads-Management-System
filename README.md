# Tracks and Treads Management System (TTMS)

## Overview
The Tracks and Treads Management System (TTMS) is a specialized software tool designed for tracking and managing images related to shoe prints in forensic and investigative contexts. This tool is particularly useful for law enforcement agencies, forensic departments, and Search and Rescue (SAR) teams that need to categorize, compare, and retrieve shoe print data efficiently. My primary use of this tool for SAR is to inventory tracks on a task for a missing subject.

## Features
- **Image Upload and Capture**: Users can upload images from their devices or capture images directly using a connected camera.
- **Image Library**: A visual library where all uploaded and captured images are stored with relevant details such as label, brand, and shoe size.
- **Detailed Image Information**: Each image can have detailed annotations including the shoe's brand and size.
- **Image Comparison**: The system includes functionality to compare new shoe prints with existing entries in the library to find matches using ORB feature detection.
- **Easy Navigation**: A user-friendly interface that allows for easy navigation and management of shoe print images.

![image](https://github.com/AlexanderMegas/Tracks-and-Treads-Management-System/assets/103082286/e429d2a9-2d88-4b2d-a159-033a93cef88b)

## Usage
To use the TTMS, typically this is done by taking photos yourself (or from others) and transferring the files to a laptop.
follow these steps after launching the application:

Upon opening the software you will be asked to select a location for the database file to be stored. Select a folder that you can reliably access and then follow the steps below to use the software.
![image](https://github.com/user-attachments/assets/9ad8bd55-ee6f-493c-8a0c-01f28493c5de)

The software will then create a database file named "inventory.db" for all your future cases. Anytime you need to re-run the software just select that file and all the data from previous cases can be looaded.
![image](https://github.com/user-attachments/assets/0c39fbba-eac4-43e3-8d4c-1e75a86b8ee0)

If there are any tables created within the database they will be loaded within the "view library" button. 

1. **Load or Create a Case Folder**: Start by loading an existing case folder or create a new one where all your image data and details will be stored. The case folder should hold all your track images for that particular case. This will create a new table within the SQL database file.

- Clicking on "Create Case" will prompt for a name. It will then verify that the case has been created.
![image](https://github.com/user-attachments/assets/7e4a237e-e9e0-4673-be06-f44766b8e2dd)
- Clicking on "Load Case" will show the current cases within the database. You can select a case (table) and it will load its content.
![image](https://github.com/user-attachments/assets/6bbb21e0-95b4-4c41-af47-766a028b8df5)

3. **View Library**: Click on 'View Image Library' to see options to capture and view your images.
   
4. **Add Images**: While in the library menu, use the 'Upload Image' or 'Capture Image' buttons to add new shoe prints to your library. You will be prompted to enter the label, brand, and size for each new image. The "capture" button currently only captures from an existing camera (if on a laptop, it will be the webcam).
![image](https://github.com/user-attachments/assets/99dbf59f-f5ae-4e6e-9162-a4c06a29e147)

5. **Inventory tread checker**: Do you have too many tracks? Or do you want to keep a collection of tracks that correspond to their owners? The button uses edge detection and other technologies to match what is in inventory to what you find in the field. It will give you a score out of 500 on the probability it is your image in inventory (self-analysis is always required so do not rely on this tool for total accuracy). It keeps a record of the tracks that you acquire and updates the data in the SQL database file accordingly. It allows you to verify accuracy and keeps memory of those tracks made in different environments and it "learns" the more images you provide.
![image](https://github.com/user-attachments/assets/baae3b30-46db-4ffa-a9f1-0fcc9f3218af)

If you verify that "no" the image is not correct it will then ask to give it a correct answer (Name, shoe size, etc.) which will then be recorded in the database.

## Installation
Download the release here: https://github.com/Doormann/Tracks-and-Treads-Management-System/releases/tag/TTMS.exe
Or 
Run it as a python program from the source code, but it does require and IDE to run. If you want to make this program portable for Windows machines I would look towards using Pysinstaller (down below).
If not, here are some other ways you can download the program.
### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- Tkinter for the GUI (usually comes with Python)
- OpenCV-Python
- Pillow (PIL Fork)

### Setup
1. **Clone the repository or download the source code:**
   ```bash
   git clone https://github.com/Doormann/Tracks-and-Treads-Management-System.git
   ```

2. **Install the required Python packages:**
   ```bash
   pip install numpy opencv-python pillow
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```
You can also turn this into an EXE by using Pyinstaller or Auto-py-to-exe.

- Pyinstaller: https://pyinstaller.org/en/stable/
- Auto-py-to-exe: https://pypi.org/project/auto-py-to-exe/
4. **Image Comparison**: Use the 'Inventory Tread Checker' to compare a newly uploaded or captured image with existing images in the database to find potential matches.

5. **Manage Data**: You can also view uploaded images, where each entry shows a thumbnail along with details like label, brand, and size formatted clearly for easy reading.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
