from logging import root
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, simpledialog
from utils.image_utils import process_image_for_edges
from utils.file_utils import save_inventory_to_db, load_inventory_from_db

def compare_images_with_orb(image_path1, image_path2):
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    return len(matches)

def match_shoe_print(label_text):
    from gui.image_display import update_image_display
    image_inventory = load_inventory_from_db()

    best_score = -1
    best_match = None

    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            edges = process_image_for_edges(file_path)

            for image_data in image_inventory:
                image_id, inventory_image_path, label, brand, size = image_data
                current_score = compare_images_with_orb(file_path, inventory_image_path)
                
                if current_score > best_score:
                    best_score = current_score
                    best_match = image_data

            if best_match:
                matched_image_label = f"{best_match[2]} - {best_match[3]} - Size: {best_match[4]}"
                label_text.set(f"Best match: {matched_image_label} with {best_score} matches")
                
                image = Image.open(file_path)
                image = ImageTk.PhotoImage(image.resize((250, 250), Image.LANCZOS))
                update_image_display(image)

                is_correct = get_user_feedback(matched_image_label, best_score)
                if is_correct:
                    print("User confirmed the match is correct.")
                else:
                    print("User indicated the match is incorrect.")
                    correct_label = simpledialog.askstring("Correct Label", "Enter the correct label for this image:", parent=root)
                    if correct_label:
                        save_inventory_to_db(file_path, correct_label, best_match[3], best_match[4])
            else:
                label_text.set("No matching image found in the inventory.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the image: {str(e)}")

def get_user_feedback(matched_image_label, match_score):
    confirmation_message = f"Is '{matched_image_label}' the correct match? Score: {match_score} matches"
    feedback = messagebox.askyesno("Match Confirmation", confirmation_message)
    return feedback
