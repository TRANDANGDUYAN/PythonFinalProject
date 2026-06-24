package dao;

import entity.DiemThi;
import utils.DatabaseConnection;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class DiemThiDAO {

    public List<Object[]> getBangDiemBySinhVien(String maSV) {
        List<Object[]> list = new ArrayList<>();
        String sql = "SELECT d.MaMon, m.TenMon, d.DiemChuyenCan, d.DiemBaiTap, d.DiemGiuaKi, d.DiemCuoiKi " +
                     "FROM DIEMTHI d JOIN MONHOC m ON d.MaMon = m.MaMon WHERE d.MaSV = ?";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, maSV);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    String maMon = rs.getString("MaMon");
                    String tenMon = rs.getString("TenMon");
                    double cc = rs.getDouble("DiemChuyenCan");
                    Double bt = rs.getDouble("DiemBaiTap");
                    if (rs.wasNull()) {
                        bt = null;
                    }
                    double gk = rs.getDouble("DiemGiuaKi");
                    double ck = rs.getDouble("DiemCuoiKi");
                    list.add(new Object[]{maMon, tenMon, cc, bt, gk, ck});
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return list;
    }

    public boolean saveOrUpdateDiem(DiemThi diem) {
        String checkSql = "SELECT COUNT(*) FROM DIEMTHI WHERE MaSV = ? AND MaMon = ?";
        String insertSql = "INSERT INTO DIEMTHI (MaSV, MaMon, DiemChuyenCan, DiemBaiTap, DiemGiuaKi, DiemCuoiKi) VALUES (?, ?, ?, ?, ?, ?)";
        String updateSql = "UPDATE DIEMTHI SET DiemChuyenCan = ?, DiemBaiTap = ?, DiemGiuaKi = ?, DiemGiuaKi = ?, DiemCuoiKi = ? WHERE MaSV = ? AND MaMon = ?";
        
        try (Connection conn = DatabaseConnection.getConnection()) {
            boolean exists = false;
            try (PreparedStatement psCheck = conn.prepareStatement(checkSql)) {
                psCheck.setString(1, diem.getMaSV());
                psCheck.setString(2, diem.getMaMon());
                try (ResultSet rs = psCheck.executeQuery()) {
                    if (rs.next() && rs.getInt(1) > 0) {
                        exists = true;
                    }
                }
            }
            
            if (exists) {
                try (PreparedStatement psUpdate = conn.prepareStatement(updateSql)) {
                    psUpdate.setDouble(1, diem.getDiemChuyenCan());
                    if (diem.getDiemBaiTap() == null) {
                        psUpdate.setNull(2, Types.DOUBLE);
                    } else {
                        psUpdate.setDouble(2, diem.getDiemBaiTap());
                    }
                    psUpdate.setDouble(3, diem.getDiemGiuaKi());
                    psUpdate.setDouble(4, diem.getDiemCuoiKi());
                    psUpdate.setString(5, diem.getMaSV());
                    psUpdate.setString(6, diem.getMaMon());
                    return psUpdate.executeUpdate() > 0;
                }
            } else {
                try (PreparedStatement psInsert = conn.prepareStatement(insertSql)) {
                    psInsert.setString(1, diem.getMaSV());
                    psInsert.setString(2, diem.getMaMon());
                    psInsert.setDouble(3, diem.getDiemChuyenCan());
                    if (diem.getDiemBaiTap() == null) {
                        psInsert.setNull(4, Types.DOUBLE);
                    } else {
                        psInsert.setDouble(4, diem.getDiemBaiTap());
                    }
                    psInsert.setDouble(5, diem.getDiemGiuaKi());
                    psInsert.setDouble(6, diem.getDiemCuoiKi());
                    return psInsert.executeUpdate() > 0;
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false;
    }
}