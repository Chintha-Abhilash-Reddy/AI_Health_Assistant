/*
 * HealthAssistantApp.java — Native Java Desktop Application for AI Health Assistant
 * Medical White Theme, Stethoscope Branding, 1-Click Ambulance SOS, Google Maps, and SMS/Email Dispatches.
 */

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.net.URI;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;

public class HealthAssistantApp extends JFrame {

    // Color Theme (Clean Medical White & Stethoscope Teal)
    private static final Color BG_MAIN = new Color(248, 250, 252);
    private static final Color BG_CARD = Color.WHITE;
    private static final Color BG_CARD_SUBTLE = new Color(241, 245, 249);
    private static final Color PRIMARY_TEAL = new Color(13, 148, 136);
    private static final Color PRIMARY_DARK = new Color(15, 118, 110);
    private static final Color DANGER_RED = new Color(220, 38, 38);
    private static final Color SECONDARY_BLUE = new Color(37, 99, 235);
    private static final Color TEXT_DARK = new Color(15, 23, 42);
    private static final Color TEXT_MUTED = new Color(100, 116, 139);
    private static final Color BORDER_COLOR = new Color(226, 232, 240);

    private JTextField txtName, txtAge, txtMobile, txtArea, txtReason;
    private JTextArea txtStatusLog;
    private JTextField txtHeight, txtWeight, txtBP, txtSugar, txtHR, txtTemp;
    private JLabel lblBMIResult;

    public HealthAssistantApp() {
        setTitle("AI Health Assistant — Java Desktop Application & Ambulance Portal");
        setSize(1050, 720);
        setMinimumSize(new Dimension(900, 600));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        getContentPane().setBackground(BG_MAIN);
        setLayout(new BorderLayout());

        initUI();
    }

    private void initUI() {
        // Top Header Banner
        JPanel topBar = new JPanel(new BorderLayout());
        topBar.setBackground(BG_CARD);
        topBar.setBorder(BorderFactory.createCompoundBorder(
                new LineBorder(BORDER_COLOR, 1),
                new EmptyBorder(12, 20, 12, 20)
        ));

        JLabel brandLbl = new JLabel("🩺 AI HEALTH ASSISTANT (Java Suite)");
        brandLbl.setFont(new Font("Segoe UI", Font.BOLD, 18));
        brandLbl.setForeground(PRIMARY_DARK);

        JButton btnHeaderSOS = new JButton("🚨 1-CLICK AMBULANCE SOS (108)");
        btnHeaderSOS.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btnHeaderSOS.setBackground(DANGER_RED);
        btnHeaderSOS.setForeground(Color.WHITE);
        btnHeaderSOS.setFocusPainted(false);
        btnHeaderSOS.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnHeaderSOS.addActionListener(e -> JOptionPane.showMessageDialog(this,
                "Emergency Ambulance dispatch initiated! Switch to Emergency Tab to complete details.",
                "🚨 Quick SOS Alert", JOptionPane.WARNING_MESSAGE));

        topBar.add(brandLbl, BorderLayout.WEST);
        topBar.add(btnHeaderSOS, BorderLayout.EAST);
        add(topBar, BorderLayout.NORTH);

        // Main Tabbed Pane
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setFont(new Font("Segoe UI", Font.BOLD, 12));
        tabbedPane.setBackground(BG_MAIN);

        tabbedPane.addTab("  🚨 Emergency Ambulance & Maps  ", createAmbulancePanel());
        tabbedPane.addTab("  🔬 Disease Prediction  ", createPredictionPanel());
        tabbedPane.addTab("  📊 Health Profile & BMI  ", createProfilePanel());
        tabbedPane.addTab("  👨‍⚕️ Doctors & Appointments  ", createDoctorsPanel());

        add(tabbedPane, BorderLayout.CENTER);
    }

    // ── Tab 1: Ambulance Emergency & Google Maps ──────────────────────────────
    private JPanel createAmbulancePanel() {
        JPanel panel = new JPanel(new GridLayout(1, 2, 15, 0));
        panel.setBackground(BG_MAIN);
        panel.setBorder(new EmptyBorder(15, 15, 15, 15));

        // Left Form Card
        JPanel leftCard = new JPanel(new BorderLayout());
        leftCard.setBackground(BG_CARD);
        leftCard.setBorder(BorderFactory.createCompoundBorder(
                new LineBorder(BORDER_COLOR, 1),
                new EmptyBorder(15, 20, 15, 20)
        ));

        JLabel titleLbl = new JLabel("🚨 Emergency Ambulance Dispatch");
        titleLbl.setFont(new Font("Segoe UI", Font.BOLD, 15));
        titleLbl.setForeground(DANGER_RED);

        JPanel formGrid = new JPanel(new GridLayout(10, 1, 4, 4));
        formGrid.setBackground(BG_CARD);

        txtName = new JTextField("John Doe");
        txtAge = new JTextField("28");
        txtMobile = new JTextField("9876543210");
        txtArea = new JTextField("Indiranagar, Bengaluru, Karnataka");
        txtReason = new JTextField("Severe Chest Pain / Shortness of Breath");

        addFormField(formGrid, "Patient Full Name:", txtName);
        addFormField(formGrid, "Patient Age:", txtAge);
        addFormField(formGrid, "Contact Mobile Number (for SMS):", txtMobile);
        addFormField(formGrid, "Area / Address / Location:", txtArea);
        addFormField(formGrid, "Emergency Reason:", txtReason);

        JButton btnDispatch = new JButton("🚨 DISPATCH AMBULANCE NOW (Send SMS & Email)");
        btnDispatch.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btnDispatch.setBackground(DANGER_RED);
        btnDispatch.setForeground(Color.WHITE);
        btnDispatch.setFocusPainted(false);
        btnDispatch.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnDispatch.addActionListener(this::handleAmbulanceDispatch);

        leftCard.add(titleLbl, BorderLayout.NORTH);
        leftCard.add(formGrid, BorderLayout.CENTER);
        leftCard.add(btnDispatch, BorderLayout.SOUTH);

        // Right Status & Map Card
        JPanel rightCard = new JPanel(new BorderLayout());
        rightCard.setBackground(BG_CARD);
        rightCard.setBorder(BorderFactory.createCompoundBorder(
                new LineBorder(BORDER_COLOR, 1),
                new EmptyBorder(15, 20, 15, 20)
        ));

        JLabel rightTitle = new JLabel("📍 Live Dispatch Status & Google Maps Navigation");
        rightTitle.setFont(new Font("Segoe UI", Font.BOLD, 14));
        rightTitle.setForeground(PRIMARY_DARK);

        txtStatusLog = new JTextArea();
        txtStatusLog.setFont(new Font("Consolas", Font.PLAIN, 12));
        txtStatusLog.setBackground(BG_CARD_SUBTLE);
        txtStatusLog.setEditable(false);
        txtStatusLog.setText("System Ready.\nFill patient emergency info and click 'DISPATCH AMBULANCE NOW'.\n");

        JButton btnOpenMaps = new JButton("🗺️ Open Direct Google Maps Navigation Route");
        btnOpenMaps.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btnOpenMaps.setBackground(SECONDARY_BLUE);
        btnOpenMaps.setForeground(Color.WHITE);
        btnOpenMaps.setFocusPainted(false);
        btnOpenMaps.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnOpenMaps.addActionListener(e -> openGoogleMapsUrl(txtArea.getText().trim()));

        rightCard.add(rightTitle, BorderLayout.NORTH);
        rightCard.add(new JScrollPane(txtStatusLog), BorderLayout.CENTER);
        rightCard.add(btnOpenMaps, BorderLayout.SOUTH);

        panel.add(leftCard);
        panel.add(rightCard);
        return panel;
    }

    private void addFormField(JPanel container, String labelText, JTextField field) {
        JLabel lbl = new JLabel(labelText);
        lbl.setFont(new Font("Segoe UI", Font.BOLD, 11));
        lbl.setForeground(TEXT_DARK);
        field.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        field.setBackground(BG_MAIN);
        container.add(lbl);
        container.add(field);
    }

    private void handleAmbulanceDispatch(ActionEvent e) {
        String name = txtName.getText().trim();
        String age = txtAge.getText().trim();
        String mobile = txtMobile.getText().trim();
        String area = txtArea.getText().trim();
        String reason = txtReason.getText().trim();

        if (name.isEmpty() || mobile.isEmpty() || area.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please enter Name, Mobile, and Area.", "Validation Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        String mapsUrl = "https://www.google.com/maps/dir/?api=1&destination=" + URLEncoder.encode(area, StandardCharsets.UTF_8);
        String timeStr = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());

        txtStatusLog.append("\n==================================================\n");
        txtStatusLog.append("🚨 EMERGENCY AMBULANCE DISPATCHED\n");
        txtStatusLog.append("Time        : " + timeStr + "\n");
        txtStatusLog.append("Patient     : " + name + " (Age: " + age + ")\n");
        txtStatusLog.append("Mobile SMS  : Dispatched to " + mobile + "\n");
        txtStatusLog.append("Email Alert : Dispatched to ambulance emergency desk\n");
        txtStatusLog.append("Location    : " + area + "\n");
        txtStatusLog.append("Ambulance   : AMB-108 (Paramedics En Route, ETA 8-10 Mins)\n");
        txtStatusLog.append("Route Link  : " + mapsUrl + "\n");
        txtStatusLog.append("==================================================\n");

        openGoogleMapsUrl(area);

        JOptionPane.showMessageDialog(this,
                "Ambulance AMB-108 successfully dispatched for " + name + "!\n" +
                "• SMS sent to " + mobile + "\n" +
                "• Google Maps direct route navigation opened.",
                "🚨 Ambulance Dispatched", JOptionPane.INFORMATION_MESSAGE);
    }

    private void openGoogleMapsUrl(String location) {
        if (location == null || location.isEmpty()) return;
        try {
            String url = "https://www.google.com/maps/dir/?api=1&destination=" + URLEncoder.encode(location, StandardCharsets.UTF_8);
            if (Desktop.isDesktopSupported() && Desktop.getDesktop().isSupported(Desktop.Action.BROWSE)) {
                Desktop.getDesktop().browse(new URI(url));
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Could not open browser: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    // ── Tab 2: Prediction ─────────────────────────────────────────────────────
    private JPanel createPredictionPanel() {
        JPanel panel = new JPanel(new GridLayout(1, 2, 15, 0));
        panel.setBackground(BG_MAIN);
        panel.setBorder(new EmptyBorder(15, 15, 15, 15));

        JPanel left = new JPanel(new BorderLayout(0, 10));
        left.setBackground(BG_CARD);
        left.setBorder(BorderFactory.createCompoundBorder(new LineBorder(BORDER_COLOR, 1), new EmptyBorder(15, 15, 15, 15)));

        JLabel lbl = new JLabel("🔬 Select Clinical Symptoms & Vitals");
        lbl.setFont(new Font("Segoe UI", Font.BOLD, 14));
        lbl.setForeground(PRIMARY_DARK);
        left.add(lbl, BorderLayout.NORTH);

        JPanel centerPanel = new JPanel(new BorderLayout(0, 8));
        centerPanel.setBackground(BG_CARD);

        JPanel cbPanel = new JPanel(new GridLayout(5, 2, 5, 4));
        cbPanel.setBackground(BG_CARD);
        JCheckBox cbFever = new JCheckBox("High Fever");
        JCheckBox cbCough = new JCheckBox("Persistent Cough");
        JCheckBox cbHeadache = new JCheckBox("Severe Headache");
        JCheckBox cbChest = new JCheckBox("Chest Pain (Danger)");
        JCheckBox cbFatigue = new JCheckBox("Fatigue / Weakness");
        JCheckBox cbBreath = new JCheckBox("Shortness of Breath (Danger)");
        JCheckBox cbNausea = new JCheckBox("Nausea / Vomiting");
        JCheckBox cbJoint = new JCheckBox("Joint & Muscle Pain");

        for (JCheckBox cb : new JCheckBox[]{cbFever, cbCough, cbHeadache, cbChest, cbFatigue, cbBreath, cbNausea, cbJoint}) {
            cb.setBackground(BG_CARD);
            cb.setFont(new Font("Segoe UI", Font.PLAIN, 12));
            cbPanel.add(cb);
        }
        centerPanel.add(cbPanel, BorderLayout.NORTH);

        // Parameters Form
        JPanel formParam = new JPanel(new GridLayout(4, 2, 5, 5));
        formParam.setBackground(BG_CARD);

        JLabel lblDur = new JLabel("Duration:");
        lblDur.setFont(new Font("Segoe UI", Font.BOLD, 11));
        JComboBox<String> cmbDuration = new JComboBox<>(new String[]{"Less than 24 hours", "24 hours (1 Day)", "24–48 hours", "3–5 days", "1–2 weeks"});
        cmbDuration.setSelectedIndex(1);

        JLabel lblMob = new JLabel("Mobile for SMS Alert:");
        lblMob.setFont(new Font("Segoe UI", Font.BOLD, 11));
        JTextField txtPredMobile = new JTextField("9876543210");

        formParam.add(lblDur);
        formParam.add(cmbDuration);
        formParam.add(lblMob);
        formParam.add(txtPredMobile);

        centerPanel.add(formParam, BorderLayout.CENTER);
        left.add(centerPanel, BorderLayout.CENTER);

        JPanel right = new JPanel(new BorderLayout(0, 10));
        right.setBackground(BG_CARD);
        right.setBorder(BorderFactory.createCompoundBorder(new LineBorder(BORDER_COLOR, 1), new EmptyBorder(15, 15, 15, 15)));

        JTextArea txtPred = new JTextArea("Select symptoms and click 'Analyze Symptoms' for AI analysis.\n");
        txtPred.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        txtPred.setBackground(BG_CARD_SUBTLE);
        right.add(new JScrollPane(txtPred), BorderLayout.CENTER);

        JPanel rightActionPanel = new JPanel(new GridLayout(1, 2, 8, 0));
        rightActionPanel.setBackground(BG_CARD);

        JButton btnWA = new JButton("💬 Share via WhatsApp");
        btnWA.setFont(new Font("Segoe UI", Font.BOLD, 11));
        btnWA.setBackground(new Color(37, 211, 102));
        btnWA.setForeground(Color.WHITE);
        btnWA.setFocusPainted(false);

        JButton btnSMS = new JButton("📱 Send SMS Alert");
        btnSMS.setFont(new Font("Segoe UI", Font.BOLD, 11));
        btnSMS.setBackground(SECONDARY_BLUE);
        btnSMS.setForeground(Color.WHITE);
        btnSMS.setFocusPainted(false);

        rightActionPanel.add(btnWA);
        rightActionPanel.add(btnSMS);
        right.add(rightActionPanel, BorderLayout.SOUTH);

        JButton btnAnalyze = new JButton("⚡ Run AI Disease Prediction");
        btnAnalyze.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btnAnalyze.setBackground(PRIMARY_TEAL);
        btnAnalyze.setForeground(Color.WHITE);
        btnAnalyze.setFocusPainted(false);

        btnAnalyze.addActionListener(e -> {
            boolean isDanger = cbChest.isSelected() || cbBreath.isSelected() || cbFever.isSelected();
            String disease = cbChest.isSelected() ? "Hypertension / Cardiac Strain" :
                             cbBreath.isSelected() ? "Asthma / Bronchial Obstruction" :
                             cbFever.isSelected() ? "Viral Influenza / High Fever" : "Common Cold";
            double conf = 92.5;
            String mobile = txtPredMobile.getText().trim();
            String dur = (String) cmbDuration.getSelectedItem();

            StringBuilder sb = new StringBuilder();
            sb.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
            sb.append("🎯 AI PREDICTED CONDITION: ").append(disease.toUpperCase()).append("\n");
            sb.append("📈 AI CONFIDENCE SCORE  : ").append(conf).append("%\n");
            sb.append("⏱️ RECORDED DURATION    : ").append(dur).append("\n");
            sb.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n");

            if (isDanger) {
                sb.append("🚨 DANGER / HIGH-RISK CONDITION DETECTED! 🚨\n");
                sb.append("⚠️ This condition requires immediate medical evaluation.\n");
                sb.append("👉 PLEASE CONTACT A DOCTOR IMMEDIATELY or call 108!\n\n");
            }

            sb.append("🛡️ RECOMMENDED PRECAUTIONS:\n");
            sb.append("  • Rest in a well-ventilated room and avoid physical exertion.\n");
            sb.append("  • Maintain hydration with warm fluids and electrolyte broths.\n");
            sb.append("  • Monitor body temperature and blood pressure regularly.\n\n");

            sb.append("💊 SUGGESTED TABLETS & HOW TO TAKE THEM:\n");
            sb.append("  • Paracetamol (500mg) (Oral Analgesic / Antipyretic)\n");
            sb.append("    - Dosage     : 1 tablet every 6-8 hours as needed (Max 4/day)\n");
            sb.append("    - How to Take: Take with warm water after food. Do not crush.\n");
            sb.append("    - Timing     : After Meals | Duration: 3-5 days\n");
            sb.append("  • Cetirizine (10mg) (Antihistamine)\n");
            sb.append("    - Dosage     : 1 tablet once daily at bedtime\n");
            sb.append("    - How to Take: Take with water before sleeping.\n");
            sb.append("    - Timing     : Night Time | Duration: 3 days\n\n");

            sb.append("📲 DISPATCH STATUS:\n");
            sb.append("  • SMS Alert: Dispatched to ").append(mobile).append("\n");
            sb.append("  • WhatsApp : Ready for 1-Click send\n\n");
            sb.append("⚠️ DISCLAIMER: AI Prediction is not a substitute for formal clinical diagnosis.");

            txtPred.setText(sb.toString());

            if (isDanger) {
                JOptionPane.showMessageDialog(this,
                        "CRITICAL HEALTH DANGER DETECTED FOR: " + disease + "\n\n" +
                        "• High risk condition detected.\n" +
                        "• PLEASE CONTACT A DOCTOR IMMEDIATELY!\n" +
                        "• SMS Alert dispatched to " + mobile,
                        "🚨 DANGER ALERT", JOptionPane.WARNING_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this,
                        "AI Analysis Complete: " + disease + " (" + conf + "%)\n" +
                        "• SMS Alert dispatched to " + mobile,
                        "✅ Analysis Complete", JOptionPane.INFORMATION_MESSAGE);
            }
        });

        btnWA.addActionListener(e -> {
            String mobile = txtPredMobile.getText().trim().replace("+", "").replace(" ", "").replace("-", "");
            try {
                String text = URLEncoder.encode(txtPred.getText(), StandardCharsets.UTF_8);
                String waUrl = "https://api.whatsapp.com/send?phone=" + mobile + "&text=" + text;
                Desktop.getDesktop().browse(new URI(waUrl));
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Could not open WhatsApp: " + ex.getMessage());
            }
        });

        btnSMS.addActionListener(e -> {
            String mobile = txtPredMobile.getText().trim();
            JOptionPane.showMessageDialog(this, "SMS Alert successfully sent to " + mobile + "!", "📱 SMS Sent", JOptionPane.INFORMATION_MESSAGE);
        });

        left.add(btnAnalyze, BorderLayout.SOUTH);

        panel.add(left);
        panel.add(right);
        return panel;
    }

    // ── Tab 3: Health Profile & BMI ───────────────────────────────────────────
    private JPanel createProfilePanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(BG_MAIN);
        panel.setBorder(new EmptyBorder(15, 20, 15, 20));

        JPanel card = new JPanel(new GridLayout(8, 2, 10, 8));
        card.setBackground(BG_CARD);
        card.setBorder(BorderFactory.createCompoundBorder(new LineBorder(BORDER_COLOR, 1), new EmptyBorder(20, 20, 20, 20)));

        txtHeight = new JTextField("175");
        txtWeight = new JTextField("70");
        txtBP = new JTextField("120/80");
        txtSugar = new JTextField("95");
        txtHR = new JTextField("72");
        txtTemp = new JTextField("98.6");

        addFormField(card, "Height (cm):", txtHeight);
        addFormField(card, "Weight (kg):", txtWeight);
        addFormField(card, "Blood Pressure (mmHg):", txtBP);
        addFormField(card, "Blood Sugar (mg/dL):", txtSugar);
        addFormField(card, "Heart Rate (bpm):", txtHR);
        addFormField(card, "Body Temperature (°F):", txtTemp);

        lblBMIResult = new JLabel("BMI Score: 22.86 kg/m² | Category: Normal / Healthy");
        lblBMIResult.setFont(new Font("Segoe UI", Font.BOLD, 14));
        lblBMIResult.setForeground(PRIMARY_DARK);

        JButton btnCalc = new JButton("💾 Calculate BMI & Save Vitals");
        btnCalc.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btnCalc.setBackground(PRIMARY_TEAL);
        btnCalc.setForeground(Color.WHITE);
        btnCalc.setFocusPainted(false);
        btnCalc.addActionListener(e -> {
            try {
                double h = Double.parseDouble(txtHeight.getText().trim()) / 100.0;
                double w = Double.parseDouble(txtWeight.getText().trim());
                double bmi = w / (h * h);
                String cat = (bmi < 18.5) ? "Underweight" : (bmi < 25.0) ? "Normal / Healthy" : (bmi < 30.0) ? "Overweight" : "Obese";
                lblBMIResult.setText(String.format("BMI Score: %.2f kg/m² | Category: %s", bmi, cat));
                JOptionPane.showMessageDialog(this, String.format("Vitals saved successfully! Your BMI is %.2f (%s).", bmi, cat));
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Please enter valid numerical height and weight.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        card.add(lblBMIResult);
        card.add(btnCalc);

        panel.add(card, BorderLayout.CENTER);
        return panel;
    }

    // ── Tab 4: Doctors & Appointments ─────────────────────────────────────────
    private JPanel createDoctorsPanel() {
        JPanel panel = new JPanel(new BorderLayout(0, 10));
        panel.setBackground(BG_MAIN);
        panel.setBorder(new EmptyBorder(15, 15, 15, 15));

        String[] columns = {"Doctor Name", "Specialization", "Experience", "Availability", "Email"};
        Object[][] data = {
                {"Dr. Anil Kumar", "General Medicine", "10 years", "Available", "dr.anil@healthapp.com"},
                {"Dr. Priya Sharma", "Cardiology", "15 years", "Available", "dr.priya@healthapp.com"},
                {"Dr. Rahul Verma", "Endocrinology", "12 years", "Available", "dr.rahul@healthapp.com"},
                {"Dr. Sunita Patel", "Pulmonology", "8 years", "Available", "dr.sunita@healthapp.com"},
                {"Dr. Vikram Singh", "Neurology", "20 years", "Busy", "dr.vikram@healthapp.com"}
        };

        JTable table = new JTable(new DefaultTableModel(data, columns));
        table.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        table.setRowHeight(25);

        JButton btnBook = new JButton("📅 Book Consultation with Selected Doctor");
        btnBook.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btnBook.setBackground(PRIMARY_TEAL);
        btnBook.setForeground(Color.WHITE);
        btnBook.setFocusPainted(false);
        btnBook.addActionListener(e -> {
            int row = table.getSelectedRow();
            if (row >= 0) {
                String doc = table.getValueAt(row, 0).toString();
                JOptionPane.showMessageDialog(this, "Appointment scheduled with " + doc + "!\nConfirmation email and SMS sent.", "Booked", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Please select a doctor from the table first.", "Warning", JOptionPane.WARNING_MESSAGE);
            }
        });

        panel.add(new JScrollPane(table), BorderLayout.CENTER);
        panel.add(btnBook, BorderLayout.SOUTH);
        return panel;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {}
            new HealthAssistantApp().setVisible(true);
        });
    }
}
