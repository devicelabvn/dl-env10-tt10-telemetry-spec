# DL-ENV10 Environmental Datalogger: Thông Tư 10/2021/TT-BTNMT Telemetry Spec, sFTP Backfill & Modbus Register Map

> **Tài liệu đặc tả kỹ thuật mở (Open Technical Specification): Cấu trúc gói tin `.txt` chuẩn Điều 39 Thông tư 10/2021/TT-BTNMT & Nghị định 53/2024/NĐ-CP, quy trình truyền dẫn sFTP/FTPS có bộ đệm Store-and-Forward và Bảng thanh ghi Modbus TCP/RTU của thiết bị Datalogger quan trắc môi trường `DL-ENV10`.**
>
> - **Đơn vị nghiên cứu & sản xuất:** **[DeviceLab](https://devicelab.vn/)** (CÔNG TY TNHH ĐẦU TƯ CÔNG NGHỆ ALPHA TECH - MST: `0111171963`)
> - **Chuyên gia biên soạn & kiểm chứng (E-E-A-T):**
>   - **[Trần Thu Hương](https://devicelab.vn/tac-gia/tran-thu-huong/)** ([English Profile](https://devicelab.vn/en/author/tran-thu-huong/)) - Quản lý Sản phẩm Kỹ thuật & Tiêu chuẩn Hợp quy (ĐHQG Hà Nội - VNU)
>   - **[Đinh Mạnh Thảo](https://devicelab.vn/tac-gia/dinh-manh-thao/)** ([English Profile](https://devicelab.vn/en/author/dinh-manh-thao/)) - Kỹ sư Trưởng R&D Hệ thống Nhúng & Firmware (PTIT)
> - **Trang thông số phần cứng chính thức:** [Datalogger Quan Trắc Môi Trường TT10 DL-ENV10](https://devicelab.vn/san-pham/dl-env10/) ([English Datasheet](https://devicelab.vn/en/products/dl-env10/))
> - **Giải pháp cho Nhà thầu Môi trường & SI:** [Datalogger Quan Trắc Môi Trường Chuẩn Thông Tư 10](https://devicelab.vn/datalogger-quan-trac-moi-truong-tt10/) ([English Solution](https://devicelab.vn/en/environmental-monitoring-datalogger/))

---

## 1. Ma Trận Đáp Ứng Kỹ Thuật Theo Điều 39 Thông Tư 10/2021/TT-BTNMT & Nghị Định 53/2024/NĐ-CP

Thiết bị **[bộ ghi dữ liệu datalogger công nghiệp DL-ENV10](https://devicelab.vn/kien-thuc/bo-ghi-du-lieu-datalogger-cong-nghiep/)** được thiết kế từ cấp độ bo mạch PCB và Firmware RTOS nhằm đáp ứng 100% yêu cầu nhận, lưu trữ, kiểm soát trạng thái và truyền dữ liệu quan trắc tự động, liên tục về Sở Tài nguyên và Môi trường (TN&MT) các tỉnh/thành phố và Bộ TN&MT:

| Hạng Mục Quy Chuẩn | Yêu Cầu Tại Điều 39 TT10/2021/TT-BTNMT | Đặc Tả Đáp Ứng Trên Phần Cứng `DeviceLab DL-ENV10` |
| :--- | :--- | :--- |
| **1. Ngõ vào thu thập dữ liệu đa kênh** | Kết nối đồng thời tín hiệu Analog (`4–20mA`, `0–10V`) và truyền thông số (`RS485 Modbus`) từ các máy phân tích tại trạm. | **Base Unit:** `4x AI` (`4–20mA` / `0–10V`, ADC Sigma-Delta 16-bit cách ly quang), `4x DI` (cách ly quang, đếm xung 10kHz), `2x DO Relay` (`250VAC/5A`), `1x RS485 Modbus RTU` cách ly `2.5kVrms`. Hỗ trợ ghép nối tối đa **03 module mở rộng I/O** (`AI-8`, `RTD/TC-4`, `DI-8`, `DO-4`, `COM-2`, `Energy 3P`). |
| **2. Định dạng tệp tin truyền dẫn** | Tệp văn bản `.txt`, bảng mã `UTF-8`, phân tách cột bằng ký tự `Tab` (`\t` - ASCII `0x09`), xuống dòng bằng `CRLF` (`\r\n`). | Tự động đóng gói tệp `[Tinh]_[CongTy]_[MaTram]_[YYYYMMDDHHMMSS].txt` chuẩn `UTF-8 without BOM`, kiểm tra toàn vẹn cú pháp trước khi đẩy lên máy chủ nhận. |
| **3. Chu kỳ truyền & Giao thức bảo mật** | Chu kỳ truyền tối đa `5 phút/lần` (hoặc theo yêu cầu cơ quan quản lý) qua giao thức `FTP` / `FTPS` / `sFTP`. | Hỗ trợ đồng thời **sFTP (SSH File Transfer Protocol - Port 22)**, **FTPS (Explicit/Implicit TLS 1.2/1.3 - Port 21/990)** và **FTP chuẩn** đẩy song song về tối đa **03 máy chủ độc lập** (Sở TN&MT, Tập đoàn/KCN, Cloud nội bộ nhà máy). |
| **4. Mã trạng thái thiết bị đo (`Status`)** | Gán đúng mã trạng thái vận hành thực tế của từng thông số đo tại thời điểm lấy mẫu. | Tự động ánh xạ tín hiệu Digital Input (`Calib_Active`, `Fault_Active`) hoặc thanh ghi Modbus từ tủ phân tích (Hach SC200/SC1000, Endress+Hauser, Horiba) sang 3 mã chuẩn: `00` (Đo bình thường), `01` (Hiệu chuẩn - Calibration), `02` (Báo lỗi thiết bị - Error). |
| **5. Lưu trữ nội bộ & Truyền bù (`Backfill`)** | Lưu trữ dữ liệu tối thiểu `60 ngày` gần nhất; tự động truyền bù dữ liệu bị gián đoạn khi có mạng trở lại. | Bộ nhớ **NOR Flash công nghiệp lưu vòng 100.000 bản ghi** kết hợp khe thẻ nhớ công nghiệp **microSD lưu > 180 ngày (`3–5 năm`)**. Cơ chế **Store-and-Forward** tự động quét hàng đợi (`Queue`) và đẩy bù toàn bộ các tệp `.txt` phát sinh trong thời gian đứt cáp quang / mất sóng 4G. |
| **6. Điều khiển máy lấy mẫu tự động & Niêm phong** | Kích hoạt máy lấy mẫu tự động khi thông số vượt ngưỡng QCVN; hỗ trợ kẹp chì niêm phong vật lý và phân quyền phần mềm. | Tích hợp sẵn thuật toán so sánh ngưỡng QCVN trên từng kênh (`pH`, `COD`, `TSS`, `NH4+-N`) để đóng rơ-le `DO1` kích hoạt **Tủ lấy mẫu nước tự động (Auto-sampler)** và gửi cảnh báo tức thời; nắp che cầu đấu hỗ trợ kẹp chì niêm phong của Sở TN&MT. |

> 📖 **Xem phân tích chuyên sâu:** [Quy chuẩn kỹ thuật Datalogger theo Điều 39 Thông tư 10/2021/TT-BTNMT](https://devicelab.vn/kien-thuc/quy-chuan-datalogger-dieu-39-thong-tu-10-2021-tt-btnmt/) · [Hướng dẫn cấu hình truyền dữ liệu quan trắc về Sở TN&MT qua FTP & sFTP](https://devicelab.vn/kien-thuc/truyen-du-lieu-quan-trac-so-tnmt-ftp-sftp/)

---

## 2. Đặc Tả Cấu Trúc Gói Tin `.txt` Chuẩn Điều 39 Thông Tư 10/2021/TT-BTNMT

### 2.1. Quy tắc đặt tên tệp và thư mục lưu trữ trên máy chủ sFTP / FTP Sở TN&MT

Khi **[thiết bị truyền dữ liệu quan trắc môi trường DL-ENV10](https://devicelab.vn/kien-thuc/thiet-bi-truyen-du-lieu-quan-trac-moi-truong/)** kết nối vào máy chủ của Sở TN&MT, tệp tin được tự động phân bổ theo cấu trúc thư mục ngày (`/[MaTram]/[YYYY]/[MM]/[DD]/`) hoặc thư mục gốc tùy theo cấu hình phần mềm tiếp nhận (như Envisoft / iLotusLand):

- **Cú pháp tên tệp chuẩn:** `[MaTinh]_[MaDoanhNghiep]_[MaTram]_[YYYYMMDDHHMMSS].txt`
  - Ví dụ trạm nước thải: `HN_KCN_NT01_20261101100000.txt`
  - Ví dụ trạm khí thải CEMS: `QN_NHAMAYNHIETDIEN_KT01_20261101100000.txt`
  - Ví dụ trạm nước ngầm (NĐ 53/2024): `BN_CONGTYABC_NN01_20261101100000.txt`
- **Quy định định dạng dòng dữ liệu (5 trường bắt buộc, phân cách bằng ký tự `Tab` `\t`):**
  ```text
  [TenThongSo]\t[GiaTriDo]\t[DonViDo]\t[ThoiGianDo_YYYYMMDDHHMMSS]\t[MaTrangThai_00_01_02]\r\n
  ```

### 2.2. Mẫu tệp `.txt` Trạm Quan Trắc Nước Thải Tự Động (`samples/HN_KCN_NT01_20261101100000.txt`)

```text
pH	7.35	pH	20261101100000	00
Temp	28.40	oC	20261101100000	00
TSS	24.80	mg/L	20261101100000	00
COD	46.20	mg/L	20261101100000	00
NH4	3.15	mg/L	20261101100000	00
Flow_In	152.60	m3/h	20261101100000	00
Flow_Out	146.90	m3/h	20261101100000	00
```

> 📂 Xem tệp mẫu thực tế tại: [`samples/HN_KCN_NT01_20261101100000.txt`](./samples/HN_KCN_NT01_20261101100000.txt)  
> 📖 **Tài liệu thiết kế trạm:** [Trạm quan trắc nước thải tự động gồm những gì? Sơ đồ & Thiết bị chuẩn TT10](https://devicelab.vn/kien-thuc/tram-quan-trac-nuoc-thai-tu-dong-gom-nhung-gi/) · [Datalogger quan trắc nước thải tự động liên tục](https://devicelab.vn/kien-thuc/datalogger-quan-trac-nuoc-thai-tu-dong/)

### 2.3. Mẫu tệp `.txt` Hệ Thống Quan Trắc Khí Thải Tự Động CEMS (`samples/QN_NHAMAYNHIETDIEN_KT01_20261101100000.txt`)

Đối với **[hệ thống quan trắc khí thải tự động CEMS](https://devicelab.vn/kien-thuc/he-thong-quan-trac-khi-thai-tu-dong-cems/)**, `DL-ENV10` hỗ trợ tính toán quy đổi nồng độ các chất ô nhiễm (`SO2`, `NOx`, `CO`, `Bụi PM`) về điều kiện chuẩn (`25°C`, `1 atm`) và hệ số oxy tham chiếu (`O2_ref`) trực tiếp trên Firmware trước khi xuất tệp `.txt`:

```text
Dust	32.40	mg/Nm3	20261101100000	00
SO2	118.50	mg/Nm3	20261101100000	00
NOx	184.20	mg/Nm3	20261101100000	00
CO	64.10	mg/Nm3	20261101100000	00
O2	6.85	%V	20261101100000	00
Temp_Flue	142.30	oC	20261101100000	00
Press_Flue	-12.40	mbar	20261101100000	00
Flow_Flue	48520.00	Nm3/h	20261101100000	00
```

> 📂 Xem tệp mẫu thực tế tại: [`samples/QN_NHAMAYNHIETDIEN_KT01_20261101100000.txt`](./samples/QN_NHAMAYNHIETDIEN_KT01_20261101100000.txt)

### 2.4. Mẫu tệp `.txt` Trạm Quan Trắc Nước Ngầm & Nước Mặt (`samples/BN_CONGTYABC_NN01_20261101100000.txt`)

Áp dụng cho giếng khoan khai thác nước dưới đất và trạm bơm nước mặt theo **Nghị định 53/2024/NĐ-CP** và **Thông tư 17/2021/TT-BTNMT**:

```text
LuuLuongTucThoi	38.60	m3/h	20261101100000	00
LuuLuongTichLuy	154820.40	m3	20261101100000	00
MucNuocGieng	-24.85	m	20261101100000	00
ChatLuong_pH	7.12	pH	20261101100000	00
ChatLuong_EC	485.00	uS/cm	20261101100000	00
```

> 📂 Xem tệp mẫu thực tế tại: [`samples/BN_CONGTYABC_NN01_20261101100000.txt`](./samples/BN_CONGTYABC_NN01_20261101100000.txt)  
> 📖 **Tài liệu chuyên khảo:** [Datalogger quan trắc khai thác nước ngầm, nước mặt tự động Nghị định 53/2024](https://devicelab.vn/kien-thuc/datalogger-quan-trac-khai-thac-nuoc-ngam-nuoc-mat-tu-dong/) · [Hệ thống quan trắc nước ngầm tự động cho giếng khoan](https://devicelab.vn/kien-thuc/he-thong-quan-trac-nuoc-ngam-tu-dong/)

---

## 3. Kiến Trúc Lưu Đệm NOR Flash & Quy Trình Truyền Bù sFTP/FTPS Tự Động (`Store-and-Forward`)

Một trong những nguyên nhân hàng đầu khiến doanh nghiệp bị nhắc nhở hoặc xử phạt hành chính là **tỷ lệ truyền nhận dữ liệu về Sở TN&MT không đạt yêu cầu** do mất sóng 4G, đứt cáp quang hoặc treo máy tính công nghiệp (IPC) chạy Windows.

Trên `DL-ENV10`, luồng thu thập và truyền dẫn được tách thành 2 tiến trình RTOS độc lập hoàn toàn, bảo vệ bởi **Hardware Watchdog Timer (WDT)** độc lập:

```text
[Đầu đo 4–20mA / RS485 Modbus]
              │
              ▼ (Chu kỳ lấy mẫu 1s – 60s, đóng gói đúng mốc 5 phút: :00, :05, :10...)
     ┌─────────────────────────────────────────────────────────────────┐
     │ TIẾN TRÌNH 1: ACQUISITION & FLASH LOGGER (Ưu tiên thời gian thực)│
     │ - Chốt nhãn thời gian thực từ chip RTC DS3231SN (đồng bộ NTP)   │
     │ - Ghi bản ghi kèm cờ `sync_flag = 0 (PENDING)` vào NOR Flash     │
     │   (100.000 bản ghi) + xuất bản sao `.txt` vào thẻ microSD        │
     └──────────────────────────────┬──────────────────────────────────┘
                                    │
                                    ▼
     ┌─────────────────────────────────────────────────────────────────┐
     │ TIẾN TRÌNH 2: sFTP / FTPS UPLOADER & BACKFILL ENGINE            │
     │ - Mở kết nối SSH sFTP (Port 22) hoặc FTPS TLS 1.2/1.3           │
     │ - Ưu tiên đẩy tệp `.txt` mới nhất để duy trì trạng thái Online  │
     │ - Quét hàng đợi `sync_flag == 0` theo thứ tự FIFO để đẩy bù     │
     │   toàn bộ các tệp `.txt` bị kẹt trong lúc mất mạng (tối đa      │
     │   20 tệp/chu kỳ) -> Xác nhận kích thước tệp -> Đổi `sync_flag=1`│
     └─────────────────────────────────────────────────────────────────┘
```

> 🛠️ **Công cụ kiểm tra tự động trong Repo này:** Chạy script [`scripts/sftp_tt10_backfill_verifier.py`](./scripts/sftp_tt10_backfill_verifier.py) để kiểm tra hợp lệ cú pháp tệp `.txt` (Tab `\t`, mã trạng thái `00/01/02`, bảng mã `UTF-8`) và mô phỏng quá trình đẩy bù sFTP lên máy chủ Sở TN&MT.  
> 📖 **Đọc thêm:** [Cơ chế lưu đệm Flash và truyền bù dữ liệu (Store & Forward) trên Datalogger](https://devicelab.vn/kien-thuc/co-che-luu-dem-flash-truyen-bu-du-lieu-datalogger/) · [So sánh FTP và sFTP trong truyền dữ liệu quan trắc môi trường](https://devicelab.vn/kien-thuc/so-sanh-ftp-va-sftp-truyen-du-lieu-quan-trac/) · [6 nguyên nhân gây mất dữ liệu trạm quan trắc và cách khắc phục triệt để](https://devicelab.vn/kien-thuc/loi-mat-du-lieu-tram-quan-trac-moi-truong/)

---

## 4. Bảng Thanh Ghi Modbus TCP Server & RS485 Modbus RTU (`DL-ENV10` Register Map)

Thiết bị **[Datalogger DL-ENV10](https://devicelab.vn/san-pham/dl-env10/)** tích hợp sẵn **Modbus TCP Server (`Port 502`, `Unit ID = 1`)** trên cổng Ethernet RJ45 `10/100Mbps`, cho phép hệ thống PLC/SCADA/HMI tại phòng điều khiển nhà máy truy xuất toàn bộ giá trị đo thời gian thực mà không làm gián đoạn luồng truyền sFTP về Sở TN&MT.

### 4.1. Thanh ghi Input Registers (`Function Code 0x04` - Kiểu `Float32 Big-Endian ABCD` & `UInt16`)

| Địa chỉ Thanh ghi (1-based) | Offset Hex (`0-based`) | Mã Kênh | Tên Thông Số & Chức Năng | Kiểu Dữ Liệu | Đơn Vị / Mã Hóa |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`30001` – `30002`** | `0x0000` | `AI1_VAL` | Giá trị quy đổi kênh Analog Input 1 (VD: `pH`) | `Float32 (ABCD)` | Theo cấu hình (`pH`, `mg/L`...) |
| **`30003` – `30004`** | `0x0002` | `AI2_VAL` | Giá trị quy đổi kênh Analog Input 2 (VD: `COD`) | `Float32 (ABCD)` | Theo cấu hình |
| **`30005` – `30006`** | `0x0004` | `AI3_VAL` | Giá trị quy đổi kênh Analog Input 3 (VD: `TSS`) | `Float32 (ABCD)` | Theo cấu hình |
| **`30007` – `30008`** | `0x0006` | `AI4_VAL` | Giá trị quy đổi kênh Analog Input 4 (VD: `NH4+-N`) | `Float32 (ABCD)` | Theo cấu hình |
| **`30009` – `30012`** | `0x0008` | `AI1..4_MA` | Dòng điện thô đo được trên 4 kênh `AI1`..`AI4` (`4000` = `4.000mA`) | `4x UInt16` | `0.001 mA` (`uA`) |
| **`30013` – `30016`** | `0x000C` | `AI1..4_STS` | Mã trạng thái Thông tư 10 của 4 kênh `AI1`..`AI4` | `4x UInt16` | `0`: Normal (`00`), `1`: Calib (`01`), `2`: Error (`02`) |
| **`30017`** | `0x0010` | `DI_BITMAP` | Trạng thái 4 ngõ vào số cách ly `DI1`..`DI4` (`Bit 0`..`Bit 3`) | `UInt16` | Bitmask (`0` = OFF, `1` = ON) |
| **`30018` – `30025`** | `0x0011` | `DI1..4_CNT` | Bộ đếm xung tích lũy 32-bit trên `DI1`..`DI4` (đồng hồ nước/lưu lượng) | `4x UInt32` | Xung (`Pulses`) |
| **`30101` – `30132`** | `0x0064` | `MB_CH1..16` | Giá trị 16 kênh đọc từ cảm biến/tủ phân tích qua RS485 Modbus RTU | `16x Float32` | Theo cấu hình (`mg/L`, `m3/h`, `oC`) |
| **`30133` – `30148`** | `0x0084` | `MB_STS1..16`| Mã trạng thái Thông tư 10 của 16 kênh Modbus RTU (`00`, `01`, `02`) | `16x UInt16` | `0`: Normal, `1`: Calib, `2`: Error |
| **`30201`** | `0x00C8` | `FTP_QUEUE` | Số lượng tệp `.txt` đang nằm trong hàng đợi chờ truyền bù (`Backfill`) | `UInt16` | Số tệp (`0` = Đã đồng bộ 100%) |
| **`30202`** | `0x00C9` | `NET_RSSI` | Cường độ sóng 4G LTE (`CSQ` / `dBm`) và trạng thái kết nối WAN | `Int16` | `dBm` (VD: `-67`) |

### 4.2. Thanh ghi Coils (`Function Code 0x01 / 0x05`) - Điều khiển Rơ-le & Chế độ Hiệu chuẩn

| Địa chỉ Coil (1-based) | Offset Hex | Mã Coil | Chức Năng Điều Khiển | Quyền Truy Cập |
| :--- | :--- | :--- | :--- | :--- |
| **`00001`** | `0x0000` | `DO1_AUTOSAMPLER` | Kích hoạt xung rơ-le `DO1` gọi máy lấy mẫu nước tự động khi vượt ngưỡng | Read / Write (`FC 01 / 05`) |
| **`00002`** | `0x0001` | `DO2_SIREN_ALARM` | Bật/tắt rơ-le `DO2` điều khiển còi đèn cảnh báo tại trạm quan trắc | Read / Write (`FC 01 / 05`) |
| **`00003`** | `0x0002` | `CALIB_MODE_ALL` | Chuyển toàn bộ các kênh của trạm sang trạng thái Hiệu chuẩn (`01`) khi bảo trì | Read / Write (`FC 01 / 05`) |
| **`00004`** | `0x0003` | `FORCE_FTP_SYNC` | Cưỡng bức đẩy tệp `.txt` tức thời và kích hoạt tiến trình truyền bù ngay lập tức | Write Single Coil (`FC 05`) |

> 📂 Tải bảng thanh ghi đầy đủ định dạng CSV (dùng để import trực tiếp vào WinCC, Ignition SCADA, KEPServerEX) tại: [`specs/dl_env10_modbus_register_map.csv`](./specs/dl_env10_modbus_register_map.csv)

---

## 5. Khả Năng Tùy Biến Phần Cứng & Ứng Dụng Mở Rộng (Campbell CR1000X, Solar Zero Export, Cấp Nước DMA)

Nhờ làm chủ hoàn toàn sơ đồ nguyên lý (Schematic), Layout PCB 4 lớp chống nhiễu EMC (`IEC 61000-4-2/4/5`) và mã nguồn Firmware C/C++ RTOS tại Việt Nam, nền tảng phần cứng `DL-ENV10` được triển khai linh hoạt cho 5 bài toán chuyên biệt:

1. **Trạm Quan Trắc Nước Thải, Khí Thải CEMS & Nước Ngầm Chuẩn Thông Tư 10:**
   - [Cẩm nang Datalogger quan trắc môi trường Thông tư 10/2021/TT-BTNMT](https://devicelab.vn/kien-thuc/cam-nang-datalogger-quan-trac-moi-truong-tt10/) ([English Handbook](https://devicelab.vn/en/articles/environmental-monitoring-datalogger-circular-10-handbook/))
   - [Tủ điện quan trắc môi trường tự động chuẩn IP65](https://devicelab.vn/kien-thuc/tu-dien-quan-trac-moi-truong-tu-dong/) ([English](https://devicelab.vn/en/articles/environmental-monitoring-control-cabinet-ip65-guide/))
   - [Kết nối và điều khiển máy lấy mẫu nước tự động qua Datalogger](https://devicelab.vn/kien-thuc/ket-noi-dieu-khien-may-lay-mau-nuoc-tu-dong-datalogger/)
   - [Kiểm định, hiệu chuẩn và quản lý mã trạng thái dữ liệu (`00/01/02`) trên Datalogger](https://devicelab.vn/kien-thuc/kiem-dinh-hieu-chuan-trang-thai-du-lieu-datalogger-quan-trac/)
   - [Báo giá Datalogger quan trắc môi trường & Cấu hình dự toán BOQ](https://devicelab.vn/kien-thuc/bao-gia-datalogger-quan-trac-moi-truong/)
2. **Giải Pháp Thay Thế Datalogger Nhập Khẩu (`Campbell Scientific CR1000X / CR300`) & Máy Tính Công Nghiệp (IPC):**
   - [Giải pháp thay thế Datalogger Campbell CR1000X, CR300 & Thiết kế OEM tại Việt Nam](https://devicelab.vn/kien-thuc/giai-phap-thay-the-datalogger-campbell-cr1000x-cr300-oem-viet-nam/) ([English](https://devicelab.vn/en/articles/campbell-scientific-cr1000x-cr300-datalogger-alternatives-oem/))
   - [So sánh Datalogger nhập khẩu và Datalogger sản xuất trong nước](https://devicelab.vn/kien-thuc/so-sanh-datalogger-nhap-khau-va-trong-nuoc/)
   - [So sánh Máy tính công nghiệp (IPC) và Datalogger nhúng RTOS trong trạm quan trắc](https://devicelab.vn/kien-thuc/so-sanh-may-tinh-cong-nghiep-ipc-va-datalogger-nhung/)
3. **Datalogger Công Nghiệp Đa Năng (`RS485 / 4–20mA / 4G LTE`) & Đấu Nối Chống Nhiễu:**
   - [Datalogger RS485 Modbus, 4–20mA & 4G LTE công nghiệp](https://devicelab.vn/kien-thuc/datalogger-rs485-modbus-4-20ma-4g-cong-nghiep/) ([English](https://devicelab.vn/en/articles/industrial-rs485-modbus-4-20ma-4g-datalogger-guide/))
   - [Cách đấu nối cảm biến 4–20mA (2 dây, 3 dây, 4 dây) vào Datalogger & PLC chống nhiễu](https://devicelab.vn/kien-thuc/cach-dau-noi-cam-bien-4-20ma-vao-datalogger-plc-chong-nhieu/)
   - [Thiết bị giám sát nhiệt độ, độ ẩm công nghiệp chuẩn GSP/Kho lạnh](https://devicelab.vn/kien-thuc/thiet-bi-giam-sat-nhiet-do-do-am-cong-nghiep/)
4. **Datalogger Điện Mặt Trời (`Solar Zero Export`) & Kết Nối SCADA EVN (`IEC 60870-5-104`):**
   - [Datalogger điện mặt trời, điều khiển bám tải Zero Export & kết nối SCADA EVN](https://devicelab.vn/kien-thuc/datalogger-dien-mat-troi-solar-zero-export-scada-evn/) ([English](https://devicelab.vn/en/articles/solar-pv-datalogger-zero-export-evn-scada-iec104/))
5. **Datalogger Áp Lực Nước, Lưu Lượng Mạng Lưới Cấp Nước DMA (`IP68 Battery-Powered`) & Thủy Văn:**
   - [Datalogger áp lực nước và lưu lượng mạng lưới cấp nước DMA chuẩn IP68](https://devicelab.vn/kien-thuc/datalogger-ap-luc-nuoc-luu-luong-cap-nuoc-dma/) ([English](https://devicelab.vn/en/articles/water-pressure-flow-datalogger-dma-ip68-guide/))
   - [Datalogger quan trắc khí tượng thủy văn và đo mưa tự động](https://devicelab.vn/kien-thuc/datalogger-quan-trac-khi-tuong-thuy-van-do-mua-tu-dong/)
   - [Quan trắc hồ chứa thủy điện và dòng chảy tối thiểu tự động](https://devicelab.vn/kien-thuc/quan-trac-ho-chua-thuy-dien-dong-chay-toi-thieu/)

---

## 6. Hệ Sinh Thái Kho Tài Liệu Mở Của DeviceLab Trên GitHub (`@devicelabvn`)

- 🌿 **[`dl-env10-tt10-telemetry-spec`](https://github.com/devicelabvn/dl-env10-tt10-telemetry-spec)** *(Repo hiện tại)*: Đặc tả gói tin `.txt` chuẩn Điều 39 Thông tư 10/2021/TT-BTNMT, script kiểm tra truyền bù sFTP và bảng thanh ghi `DL-ENV10`.
- ⚡ **[`dl-gw200-modbus-mqtt-edge`](https://github.com/devicelabvn/dl-gw200-modbus-mqtt-edge)**: Mẫu JSON Payload MQTT TLS 1.3, cấu hình Multi-Master Caching (`< 2ms`) & Store-and-Forward của [`DL-GW200`](https://devicelab.vn/san-pham/dl-gw200/) và [`DL-RS485`](https://devicelab.vn/san-pham/dl-rs485/).
- 📘 **[`devicelab-iot-hardware-handbook`](https://github.com/devicelabvn/devicelab-iot-hardware-handbook)**: Sổ tay [thiết kế mạch điện tử](https://devicelab.vn/thiet-ke-mach-dien-tu/), [dịch vụ thiết kế PCB](https://devicelab.vn/kien-thuc/dich-vu-thiet-ke-pcb/), [sản xuất bo mạch điện tử công nghiệp](https://devicelab.vn/kien-thuc/san-xuat-bo-mach-dien-tu-cong-nghiep/) và [công ty lập trình nhúng Firmware IoT](https://devicelab.vn/kien-thuc/cong-ty-lap-trinh-nhung-firmware-iot/).
- 🔌 **[`dl-gw400-node-red-python-edge-examples`](https://github.com/devicelabvn/dl-gw400-node-red-python-edge-examples)**: Kiến trúc Multi-bus RS485 Polling trên [`DL-GW400`](https://devicelab.vn/san-pham/dl-gw400/) và mẫu Node-RED / Python Edge.

---

## 7. Liên Hệ Tư Vấn Kỹ Thuật, Đặt Mẫu PoC & Nhận Hồ Sơ Thầu (`BOQ / Datasheet`)

- **Đơn vị sản xuất:** CÔNG TY TNHH ĐẦU TƯ CÔNG NGHỆ ALPHA TECH (**[DeviceLab](https://devicelab.vn/)**) - Mã số thuế: `0111171963`
- **Địa chỉ R&D Lab:** Số 32/4, Hà Trì 4, Phường Hà Đông, TP. Hà Nội, Việt Nam
- **Hotline / Zalo Kỹ sư trưởng ([Đinh Mạnh Thảo](https://devicelab.vn/tac-gia/dinh-manh-thao/)):** `0982 503 355`
- **Email hỗ trợ dự án:** `contact@devicelab.vn` | `hi@devicelab.vn`
- **Đăng ký mượn thiết bị Demo 7 ngày / Nhận báo giá SI & OEM:** [https://devicelab.vn/san-pham/dl-env10/](https://devicelab.vn/san-pham/dl-env10/) | [Gửi yêu cầu kỹ thuật](https://devicelab.vn/gui-yeu-cau/)
