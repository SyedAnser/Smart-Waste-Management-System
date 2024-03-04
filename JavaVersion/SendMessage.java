import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

class SendMessage extends JFrame
{
    private JTextField textField;
    private Container c;

    public SendMessage() {
		setBounds(100, 100, 450, 300);        
        setDefaultCloseOperation(EXIT_ON_CLOSE);


        c = getContentPane();
        c.setBackground(new Color(0, 0, 163));
        c.setLayout(null);
		
		textField.setText("Dustbin is full. Administration will send someone to clear it");
		textField.setFont(new Font("Tahoma", Font.BOLD, 15));
        textField.setBounds(33, 10, 377, 117);
		c.add(textField);
        
        setVisible(true);
		
	}

}
