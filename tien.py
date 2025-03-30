import subprocess
import time
import cv2
import pytesseract

def tap(x, y):
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])

def swipe(x1, y1, x2, y2, duration=500):
    subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

def get_screen_text():
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/screen.png"])
    subprocess.run(["adb", "pull", "/sdcard/screen.png", "screen.png"])
    image = cv2.imread("screen.png")
    text = pytesseract.image_to_string(image)
    return text.lower()

def login_gmail(email, password):
    print(f"Đang đăng nhập vào Gmail: {email}")
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "https://accounts.google.com/ServiceLogin"])
    time.sleep(5)
    tap(500, 800)
    subprocess.run(["adb", "shell", "input", "text", email])
    tap(900, 1200)
    time.sleep(5)
    tap(500, 1000)
    subprocess.run(["adb", "shell", "input", "text", password])
    tap(900, 1400)
    time.sleep(5)
    print("Đăng nhập hoàn tất!")

def start_watching_ads():
    print("Đang xem quảng cáo...")
    start_time = time.time()
    while True:
        text = get_screen_text()
        if "x" in text or "skip" in text or "done" in text:
            tap(1000, 100)
            break
        time.sleep(5)
    end_time = time.time()
    duration = end_time - start_time
    return duration

def main():
    accounts = []
    total_money = 0
    money_per_second = 10

    num_accounts = int(input("Nhập số tài khoản (1-5): "))
    for i in range(num_accounts):
        email = input(f"Nhập email tài khoản {i+1}: ")
        password = input(f"Nhập mật khẩu tài khoản {i+1}: ")
        accounts.append((email, password))

    for email, password in accounts:
        login_gmail(email, password)
        print(f"Đang mở ứng dụng Samsung Global Goals cho {email}...")
        subprocess.run(["adb", "shell", "monkey", "-p", "com.samsung.globalgoals", "-c", "android.intent.category.LAUNCHER", "1"])
        time.sleep(3)
        
        total_time = 0
        while True:
            text = get_screen_text()
            if "watch ad" in text or "xem quảng cáo" in text:
                tap(500, 1700)
                duration = start_watching_ads()
                total_time += duration
                print(f"Tài khoản {email} coi QC hết {duration:.2f} giây")
            
            command = input("Nhập 'stop' để dừng hoặc Enter để tiếp tục: ")
            if command.lower() == "stop":
                break
        
        earned_money = total_time * money_per_second
        total_money += earned_money
        print(f"Tài khoản {email} đã góp được {earned_money} đồng.")

    print(f"Tất cả tài khoản đã góp được tổng cộng {total_money} đồng.")
    
    goals = [
        "1. Xóa đói",
        "2. Xóa nghèo",
        "3. Sức khỏe tốt",
        "4. Giáo dục chất lượng",
        "5. Bình đẳng giới",
        "6. Nước sạch",
        "7. Năng lượng sạch",
        "8. Tăng trưởng kinh tế",
        "9. Công nghiệp và đổi mới",
        "10. Giảm bất bình đẳng",
        "11. Thành phố bền vững",
        "12. Sản xuất và tiêu dùng",
        "13. Hành động khí hậu",
        "14. Bảo vệ đại dương",
        "15. Bảo vệ rừng",
        "16. Công lý và hòa bình",
        "17. Hợp tác toàn cầu"
    ]

    for goal in goals:
        print(goal)
    
    choice = int(input("Chọn số mục tiêu bạn muốn quyên góp: "))
    print(f"Đã chọn quyên góp toàn bộ số tiền ({total_money} đồng) cho mục tiêu: {goals[choice - 1]}")

if __name__ == "__main__":
    main()
