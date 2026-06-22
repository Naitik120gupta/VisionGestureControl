# 🤖 GestureScroll  
### Hand Gesture Controlled Instagram Reels Scroller

GestureScroll is a **computer vision–based automation project** that allows users to scroll through Instagram Reels using **hand gestures only** — no mouse, no keyboard, just a webcam and real-time gesture recognition.

This project demonstrates how **human–computer interaction (HCI)** can be enhanced using **touchless controls** powered by AI and computer vision.

---

## 🚀 Features

- ✋ Real-time hand gesture recognition
- 🎥 Webcam-based interaction
- 🖱️ Touchless scrolling (no physical input devices)
- ⚡ Lightweight and fast execution
- 🧠 Simple yet powerful gesture logic

---

## 🛠️ Tech Stack

- **MediaPipe** – Real-time hand landmark detection  
- **OpenCV** – Camera input and video frame processing  
- **PyAutoGUI** – Automating scroll/keyboard actions  

---

## 🎯 How It Works

1. Open **Instagram Reels** in a web browser.
2. Run the GestureScroll script.
3. Place your hand in front of the webcam.
4. Perform swipe gestures:
   - 👉 Swipe Right → Scroll to next reel
   - 👈 Swipe Left → Scroll to previous reel
5. Enjoy hands-free scrolling ✨

### Mobile / Android Mode

You can also use the same gesture detection to control reels on an Android phone through `adb`:

1. Enable Developer Options and USB Debugging on your phone.
2. Connect the phone to your computer and confirm `adb devices` shows it.
3. Start the app with `--target android`.

Example:

```bash
python main.py --target android
```

In Android mode, a downward hand gesture triggers an upward swipe on the phone screen, which matches the way reels are advanced.

---

## 💡 Use Case

GestureScroll is a **fun experimental project** showcasing:
- Gesture recognition
- Touchless user interfaces
- Automation using computer vision

It provides a glimpse into future applications such as:
- Smart interfaces
- Accessibility tools
- AR/VR interaction systems
- Touchless control systems

---

## 🧪 Project Type

- Computer Vision
- Human–Computer Interaction (HCI)
- Automation
- Experimental / Learning Project

---

## 📌 Future Improvements

- Add vertical swipe support
- Gesture sensitivity calibration
- Multi-platform support
- Custom gesture mapping
- UI overlay for feedback
- Bluetooth / wireless phone control

---

## 👨‍💻 Author

**Naitik Gupta**  
Backend | AI | Blockchain | Cybersecurity  

📷 Instagram: https://instagram.com/geeksecurity_/
💻 GitHub: https://github.com/naitik120gupta

---

⭐ If you find this project useful or interesting, consider starring the repository!
