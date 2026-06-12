import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def show_devices(devices_list):
    logger.debug(f"Hiển thị danh sách {len(devices_list)} thiết bị")

    if not devices_list:
        print("Hệ thống hiện chưa có thiết bị giám sát nào!")
        return

    print("\n── DANH SÁCH THIẾT BỊ GIÁM SÁT ──")
    print(f"{'MÃ TB':<6}| {'VỊ TRÍ PHÂN XƯỞNG':<25}| {'CHỈ SỐ CŨ':>10}| {'CHỈ SỐ MỚI':>10}| {'TRẠNG THÁI':<10}")
    print("-" * 75)

    for device in devices_list:
        print(f"{device['id']:<6}| {device['location']:<25}| {device['old_index']:>10.0f}| {device['new_index']:>10.0f}| {device['status']:<10}")
        

def update_indices(devices_list):
    logger.debug("Thực hiện cập nhật chỉ số điện")

    if not devices_list:
        print("Danh sách thiết bị trống!")
        return

    device_id = input("Nhập mã thiết bị: ").strip().upper()

    device = None
    for item in devices_list:
        if item["id"] == device_id:
            device = item
            break

    if device is None:
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!")
        return

    while True:
        try:
            old_index = float(input("Nhập chỉ số cũ: "))
            if old_index < 0:
                raise ValueError
            break
        except ValueError:
            logger.error("Sai định dạng chỉ số cũ")
            print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")

    while True:
        try:
            new_index = float(input("Nhập chỉ số mới: "))

            if new_index < 0:
                raise ValueError

            if new_index < old_index:
                print("[Lỗi] (ERR-E02): Số liệu lỗi! Chỉ số mới không được nhỏ hơn chỉ số cũ!")
                continue

            break

        except ValueError:
            logger.error("Sai định dạng chỉ số mới")
            print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")

    device["old_index"] = old_index
    device["new_index"] = new_index

    logger.info(f"Đã cập nhật chỉ số cho {device_id}")
    print(f"[Thành công]: Thiết bị {device_id} đã được cập nhật số liệu mới")


def trigger_overload_alert(devices_list):
    logger.debug("Kiểm tra cảnh báo quá tải")

    if not devices_list:
        print("Danh sách thiết bị trống!")
        return

    device_id = input("Nhập mã thiết bị cần duyệt: ").strip().upper()

    device = None
    for item in devices_list:
        if item["id"] == device_id:
            device = item
            break

    if device is None:
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!")
        return

    if device["status"] == "Overload":
        print("[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!")
        return

    consumption = device["new_index"] - device["old_index"]

    print(f"Tìm thấy thiết bị tại: {device['location']} (Lượng tiêu thụ: {consumption:.0f} kWh)")

    if consumption > 5000:
        device["status"] = "Overload"

        logger.warning(f"[Cảnh báo]: Thiết bị {device_id} đã vượt ngưỡng tiêu thụ an toàn, chuyển sang OVERLOAD!")

        print(f"[Thành công]: Thiết bị {device_id} đã được kích hoạt trạng thái OVERLOAD!")
    else:
        print("Thiết bị chưa vượt ngưỡng tiêu thụ an toàn.")


def calculate_energy_financials(devices_list):
    logger.debug(f"Đang tính toán chi phí năng lượng cho {len(devices_list)} thiết bị")

    if not devices_list:
        return 0.0, 0.0, 0.0

    total_kwh = 0

    for device in devices_list:
        total_kwh += device["new_index"] - device["old_index"]

    total_cost = total_kwh * 3000

    discount_percent = 0

    if total_kwh >= 50000:
        discount_percent = 3

    final_cost = total_cost - (total_cost * discount_percent / 100)

    return total_kwh, discount_percent, final_cost


def show_financial_report(devices_list):
    total_kwh, discount_percent, final_cost = calculate_energy_financials(devices_list)

    print("\n── BÁO CÁO NĂNG LƯỢNG ──")
    print(f"Tổng lượng điện tiêu thụ : {total_kwh:,.0f} kWh")
    print(f"Chiết khấu áp dụng       : {discount_percent}%")
    print(f"Tổng tiền phải thanh toán: {final_cost:,.0f} VND")


def main():
    devices_list = [
        {
            "id": "M01",
            "location": "Mechanical Shop A",
            "old_index": 1200,
            "new_index": 4500,
            "status": "Normal"
        },
        {
            "id": "M02",
            "location": "Assembly Line B",
            "old_index": 2300,
            "new_index": 8500,
            "status": "Overload"
        }
    ]

    while True:
        print("\n" + "=" * 60)
        print("SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN")
        print("=" * 60)
        print("1. Xem danh sách thiết bị giám sát")
        print("2. Cập nhật chỉ số điện tiêu thụ (Check-in)")
        print("3. Kích hoạt trạng thái cảnh báo quá tải")
        print("4. Tính tổng lượng điện & Chi phí năng lượng")
        print("5. Thoát chương trình")
        print("=" * 60)

        try:
            choice = int(input("\nMời chọn chức năng (1-5): "))

            if choice == 1:
                show_devices(devices_list)

            elif choice == 2:
                update_indices(devices_list)

            elif choice == 3:
                trigger_overload_alert(devices_list)

            elif choice == 4:
                show_financial_report(devices_list)

            elif choice == 5:
                print("Thoát chương trình...")
                break

            else:
                print("[Lỗi] (ERR-E05): Lựa chọn sai! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 5!")

        except ValueError:
            logger.error("Người dùng nhập sai định dạng menu")
            print("[Lỗi] (ERR-E05): Lựa chọn sai! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 5!")


main()