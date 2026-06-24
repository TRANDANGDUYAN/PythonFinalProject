package ui;

import dao.DiemThiDAO;
import dao.MonHocDAO;
import entity.DiemThi;
import entity.MonHoc;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;
import java.awt.*;
import java.util.List;

@SuppressWarnings("serial")
public class ManageGradesDialog extends JDialog {

    private JTable table;
    private DefaultTableModel model;
    private JComboBox<MonHoc> cbMonHoc;
    private JTextField txtCC, txtBT, txtGK, txtCK;
    private JButton btnSave;
    private JLabel lblGpa;

    private String currentMaSV;
    private DiemThiDAO diemThiDAO;
    private MonHocDAO monHocDAO;

    public ManageGradesDialog(JFrame parent, String maSV, String hoTen) {
        super(parent, "Quản Lý Điểm Số - " + hoTen + " (" + maSV + ")", true);
        this.currentMaSV = maSV;
        this.diemThiDAO = new DiemThiDAO();
        this.monHocDAO = new MonHocDAO();

        setSize(850, 500);
        setLocationRelativeTo(parent);
        setLayout(new BorderLayout(10, 10));
        
        // nhap diem
        JPanel pnlTop = new JPanel(new GridBagLayout());
        pnlTop.setBorder(new EmptyBorder(15, 15, 10, 15));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 15);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0;
        JLabel lblMonHoc = new JLabel("Môn học:");
        lblMonHoc.setFont(new Font("Arial", Font.BOLD, 12));
        pnlTop.add(lblMonHoc, gbc);

        gbc.gridx = 1; gbc.gridy = 0; gbc.gridwidth = 3;
        cbMonHoc = new JComboBox<>();
        cbMonHoc.setBackground(Color.WHITE);
        pnlTop.add(cbMonHoc, gbc);
        gbc.gridwidth = 1;

        gbc.gridx = 0; gbc.gridy = 1; pnlTop.add(new JLabel("Chuyên cần (CC):"), gbc);
        gbc.gridx = 1; gbc.gridy = 1; txtCC = new JTextField(8); pnlTop.add(txtCC, gbc);

        gbc.gridx = 2; gbc.gridy = 1; pnlTop.add(new JLabel("Bài tập (Trống = Loại 2):"), gbc);
        gbc.gridx = 3; gbc.gridy = 1; txtBT = new JTextField(8); pnlTop.add(txtBT, gbc);

        gbc.gridx = 0; gbc.gridy = 2; pnlTop.add(new JLabel("Giữa kỳ (GK):"), gbc);
        gbc.gridx = 1; gbc.gridy = 2; txtGK = new JTextField(8); pnlTop.add(txtGK, gbc);

        gbc.gridx = 2; gbc.gridy = 2; pnlTop.add(new JLabel("Cuối kỳ (CK):"), gbc);
        gbc.gridx = 3; gbc.gridy = 2; txtCK = new JTextField(8); pnlTop.add(txtCK, gbc);

        gbc.gridx = 4; gbc.gridy = 2;
        btnSave = new JButton("Lưu Điểm");
        btnSave.setBackground(new Color(0, 102, 153)); 
        btnSave.setForeground(Color.WHITE);
        btnSave.setFont(new Font("Arial", Font.BOLD, 12));
        pnlTop.add(btnSave, gbc);

        add(pnlTop, BorderLayout.NORTH);

        // bang diem
        JPanel pnlCenter = new JPanel(new BorderLayout());
        pnlCenter.setBorder(new EmptyBorder(0, 15, 0, 15));

        String[] cols = {"Mã Môn", "Tên Môn Học", "CC", "BT", "GK", "CK", "Tổng", "Chữ"};
        model = new DefaultTableModel(cols, 0); 
        table = new JTable(model);
        table.setRowHeight(25);
        
        JTableHeader header = table.getTableHeader();
        header.setBackground(new Color(0, 102, 170));
        header.setForeground(Color.WHITE);
        header.setFont(new Font("Arial", Font.BOLD, 12));

        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(JLabel.CENTER);
        for (int i = 0; i < table.getColumnCount(); i++) {
            if (i != 1) table.getColumnModel().getColumn(i).setCellRenderer(centerRenderer);
        }
        table.getColumnModel().getColumn(0).setPreferredWidth(60);
        table.getColumnModel().getColumn(1).setPreferredWidth(200);

        pnlCenter.add(new JScrollPane(table), BorderLayout.CENTER);
        add(pnlCenter, BorderLayout.CENTER);

        // gpa
        JPanel pnlFooter = new JPanel(new FlowLayout(FlowLayout.LEFT));
        pnlFooter.setBorder(new EmptyBorder(10, 15, 10, 15));
        
        lblGpa = new JLabel("GPA Tích lũy (Hệ 4.0): Chưa có điểm");
        lblGpa.setFont(new Font("Arial", Font.BOLD, 16));
        lblGpa.setForeground(new Color(204, 51, 0)); 
        pnlFooter.add(lblGpa);

        add(pnlFooter, BorderLayout.SOUTH);

        loadMonHocToComboBox();
        loadGradesToTable();
        addEvents();
    }

    private void loadMonHocToComboBox() {
        cbMonHoc.removeAllItems();
        List<MonHoc> list = monHocDAO.getAllMonHoc();
        for (MonHoc mh : list) {
            cbMonHoc.addItem(mh);
        }
    }

    private void loadGradesToTable() {
        model.setRowCount(0);
        List<Object[]> bangDiem = diemThiDAO.getBangDiemBySinhVien(currentMaSV);
        
        List<MonHoc> dsMonHoc = monHocDAO.getAllMonHoc();
        
        double tongDiemHeSoTichLuy = 0;
        int tongSoTinChi = 0;

        for (Object[] row : bangDiem) {
            String maMon = (String) row[0];
            String tenMon = (String) row[1];
            double cc = (double) row[2];
            Double bt = (Double) row[3];
            double gk = (double) row[4];
            double ck = (double) row[5];
            
            int tinChi = 0;
            for (MonHoc mh : dsMonHoc) {
                if (mh.getMaMon().equals(maMon)) {
                    tinChi = mh.getSoTinChi();
                    break;
                }
            }
            
            double total = 0;
            if (bt != null) {
                total = cc * 0.1 + bt * 0.2 + gk * 0.2 + ck * 0.5;
            } else {
                total = cc * 0.2 + gk * 0.2 + ck * 0.6;
            }
            total = Math.round(total * 10.0) / 10.0;

            String letter = getLetterGrade(total);
            double gpa4 = getGpaPoint(letter);

            tongDiemHeSoTichLuy += gpa4 * tinChi;
            tongSoTinChi += tinChi;

            model.addRow(new Object[]{
                maMon, tenMon, cc, (bt != null ? bt : "-"), gk, ck, total, letter
            });
        }

        if (tongSoTinChi > 0) {
            double gpa = tongDiemHeSoTichLuy / tongSoTinChi;
            lblGpa.setText(String.format("GPA Tích lũy (Hệ 4.0): %.2f", gpa));
        } else {
            lblGpa.setText("GPA Tích lũy (Hệ 4.0): Chưa có điểm");
        }
    }

    private String getLetterGrade(double total) {
        if (total >= 8.5) return "A";
        if (total >= 8.0) return "B+";
        if (total >= 7.0) return "B";
        if (total >= 6.5) return "C+";
        if (total >= 5.5) return "C";
        if (total >= 5.0) return "D+";
        if (total >= 4.0) return "D";
        return "F";
    }

    // Quy đổi Hệ 4.0 chuẩn mực
    private double getGpaPoint(String letter) {
        switch (letter) {
            case "A": return 4.0;
            case "B+": return 3.5;
            case "B": return 3.0;
            case "C+": return 2.5;
            case "C": return 2.0;
            case "D+": return 1.5;
            case "D": return 1.0;
            default: return 0.0;
        }
    }

    private void addEvents() {
        cbMonHoc.addActionListener(e -> {
            MonHoc mh = (MonHoc) cbMonHoc.getSelectedItem();
            if (mh != null) {
                if (mh.getLoaiMon() == 2) {
                    txtBT.setText("");
                    txtBT.setEnabled(false);
                    txtBT.setBackground(new Color(220, 220, 220));
                } else {
                    txtBT.setEnabled(true);
                    txtBT.setBackground(Color.WHITE);
                }
            }
        });

        table.getSelectionModel().addListSelectionListener(e -> {
            int row = table.getSelectedRow();
            if (row >= 0) {
                String maMon = model.getValueAt(row, 0).toString();
                for (int i = 0; i < cbMonHoc.getItemCount(); i++) {
                    if (cbMonHoc.getItemAt(i).getMaMon().equals(maMon)) {
                        cbMonHoc.setSelectedIndex(i);
                        break;
                    }
                }
                txtCC.setText(model.getValueAt(row, 2).toString());
                String btVal = model.getValueAt(row, 3).toString();
                txtBT.setText(btVal.equals("-") ? "" : btVal);
                txtGK.setText(model.getValueAt(row, 4).toString());
                txtCK.setText(model.getValueAt(row, 5).toString());
            }
        });

        btnSave.addActionListener(e -> {
            try {
                MonHoc mh = (MonHoc) cbMonHoc.getSelectedItem();
                double cc = Double.parseDouble(txtCC.getText());
                double gk = Double.parseDouble(txtGK.getText());
                double ck = Double.parseDouble(txtCK.getText());
                Double bt = null;

                if (mh.getLoaiMon() == 1) { 
                    bt = Double.parseDouble(txtBT.getText());
                }

                if (cc < 0 || cc > 10 || gk < 0 || gk > 10 || ck < 0 || ck > 10 || (bt != null && (bt < 0 || bt > 10))) {
                    JOptionPane.showMessageDialog(this, "Điểm phải nằm trong khoảng từ 0 đến 10!");
                    return;
                }

                DiemThi diem = new DiemThi(currentMaSV, mh.getMaMon(), cc, bt, gk, ck);
                if (diemThiDAO.saveOrUpdateDiem(diem)) {
                    JOptionPane.showMessageDialog(this, "Lưu điểm thành công!");
                    loadGradesToTable();
                    txtCC.setText(""); txtBT.setText(""); txtGK.setText(""); txtCK.setText("");
                    table.clearSelection();
                } else {
                    JOptionPane.showMessageDialog(this, "Lưu điểm thất bại!");
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập định dạng số hợp lệ vào các ô điểm!");
            }
        });
    }
}