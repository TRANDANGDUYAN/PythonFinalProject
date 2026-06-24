package entity;

public class DiemThi {
    
    private String maSV;
    private String maMon;
    private double diemChuyenCan;
    private Double diemBaiTap;
    private double diemGiuaKi;
    private double diemCuoiKi;

    public DiemThi() {
    }

    public DiemThi(String maSV, String maMon, double diemChuyenCan, Double diemBaiTap, double diemGiuaKi, double diemCuoiKi) {
        this.maSV = maSV;
        this.maMon = maMon;
        this.diemChuyenCan = diemChuyenCan;
        this.diemBaiTap = diemBaiTap;
        this.diemGiuaKi = diemGiuaKi;
        this.diemCuoiKi = diemCuoiKi;
    }

    public String getMaSV() {
        return maSV;
    }

    public void setMaSV(String maSV) {
        this.maSV = maSV;
    }

    public String getMaMon() {
        return maMon;
    }

    public void setMaMon(String maMon) {
        this.maMon = maMon;
    }

    public double getDiemChuyenCan() {
        return diemChuyenCan;
    }

    public void setDiemChuyenCan(double diemChuyenCan) {
        this.diemChuyenCan = diemChuyenCan;
    }

    public Double getDiemBaiTap() {
        return diemBaiTap;
    }

    public void setDiemBaiTap(Double diemBaiTap) {
        this.diemBaiTap = diemBaiTap;
    }

    public double getDiemGiuaKi() {
        return diemGiuaKi;
    }

    public void setDiemGiuaKi(double diemGiuaKi) {
        this.diemGiuaKi = diemGiuaKi;
    }

    public double getDiemCuoiKi() {
        return diemCuoiKi;
    }

    public void setDiemCuoiKi(double diemCuoiKi) {
        this.diemCuoiKi = diemCuoiKi;
    }
}