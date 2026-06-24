package entity;

public class MonHoc {
    
    private String maMon;
    private String tenMon;
    private int soTinChi;
    private int loaiMon;
    private String maKhoa;

    public MonHoc() {
    }

    public MonHoc(String maMon, String tenMon, int soTinChi, int loaiMon, String maKhoa) {
        this.maMon = maMon;
        this.tenMon = tenMon;
        this.soTinChi = soTinChi;
        this.loaiMon = loaiMon;
        this.maKhoa = maKhoa;
    }

    public String getMaMon() {
        return maMon;
    }

    public void setMaMon(String maMon) {
        this.maMon = maMon;
    }

    public String getTenMon() {
        return tenMon;
    }

    public void setTenMon(String tenMon) {
        this.tenMon = tenMon;
    }

    public int getSoTinChi() {
        return soTinChi;
    }

    public void setSoTinChi(int soTinChi) {
        this.soTinChi = soTinChi;
    }

    public int getLoaiMon() {
        return loaiMon;
    }

    public void setLoaiMon(int loaiMon) {
        this.loaiMon = loaiMon;
    }

    public String getMaKhoa() {
        return maKhoa;
    }

    public void setMaKhoa(String maKhoa) {
        this.maKhoa = maKhoa;
    }

    @Override
    public String toString() {
        return tenMon;
    }
}