import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;


class DisplayData extends JFrame implements ActionListener
{
    private Container c;
    private JLabel title;
    private JButton refresh;
    private JButton clear;
    private JTextArea tout;
    private JTextArea status;
    private JLabel utitle;
    static String ToPrint = "";
    DrawGraph graph = new DrawGraph();
    
    public DisplayData()
    {
        setTitle("Sensors Data");
        setBounds(300,90,900,700);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(true);
        
        c = getContentPane();
        c.setBackground(new Color(0, 0, 163));
        c.setLayout(null);
        
        title = new JLabel("Sensors Data");
        title.setForeground (Color.white);
        title.setSize(300, 30);
        title.setLocation(300, 30);
        c.add(title);
        
        refresh = new JButton("Refresh");
        refresh.setSize(100, 20);
        refresh.setLocation(150, 550);
        refresh.addActionListener(this);
        c.add(refresh);
        
        clear = new JButton("Reset");
        clear.setSize(100, 20);
        clear.setLocation(270, 550);
        clear.addActionListener(this);
        c.add(clear);
        
        utitle = new JLabel();
        utitle.setSize(200, 50);
        utitle.setText("Dustbin Status");
        utitle.setForeground(Color.white);
        utitle.setLocation(100,100);
        c.add(utitle);
        
        status = new JTextArea();
        status.setSize(125, 25);
        status.setLocation(100, 150);
        status.setEditable(false);
        c.add(status);
        
        tout = new JTextArea();
        tout.setSize(300, 400);
        tout.setLocation(550, 100);
        tout.setLineWrap(true);
        tout.setEditable(false);
        tout.setText("Ultrasonic Sensor Data");
        c.add(tout);
        
        JPanel app = new JPanel();
        app.add(graph);
        app.setSize(400, 400);
        app.setLocation(100, 200);
                
        c.add(app); 
        
        setVisible(true);
    }
    
    
    public void actionPerformed(ActionEvent e)
    {
        DataExtract ds = new DataExtract();
        
        java.util.List al = ds.Ultrasonic(ds.getUrlContents("https://api.thingspeak.com/channels/1914670/feeds.json?results=2"));
        java.util.List <Integer> value = al.subList(al.size()-10, al.size());
        int size = value.size();
        
        int element = (Integer)(value.get(size-1));
        String x = "" + element;
        if(element <=3)
        {
        x = " Dustbin is FULL";
        SendMessage s = new SendMessage();
        }
        else
        x = " Dustbin is not full";
        
        if (e.getSource() == refresh)
        {    
            graph = new DrawGraph(value);
            JPanel app = new JPanel();
            app.add(graph);
            app.setSize(400, 400);
            app.setLocation(100, 200);
                
            c.add(app); 
            
            status.setText(x);
            tout.setText("Ultrasonic Sensor Data \n"+ value.toString());
        }
        
        if(e.getSource() == clear)
        {
            graph = new DrawGraph(Arrays.asList());
            JPanel app = new JPanel();
            app.add(graph);
            app.setSize(400, 400);
            app.setLocation(100, 200);
                
            c.add(app); 
            tout.setText("");
            status.setText("");
        }
    }
    
    public static void main(String[] args) throws Exception
    {
        DisplayData f = new DisplayData();
    }
}
