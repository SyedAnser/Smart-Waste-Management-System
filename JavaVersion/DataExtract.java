
import java.net.*;
import java.util.*;
import java.io.*;
import java.lang.*;

public class DataExtract{
    
    public static List dist = new ArrayList();

    public static void run()
    {
        String Url1="https://api.thingspeak.com/channels/1914670/feeds.json?results=2";
        String output1= getUrlContents(Url1);
        
        String Url2 ="https://api.thingspeak.com/channels/1917496/feeds.json?results=2";        
        String output2= getUrlContents(Url2);

        dist = Ultrasonic(output1);
        List temp = DHT(output2);        
    }
    
    public static void main(String[] args)
    {
        run();
        System.out.println(dist);
    }
    
    public static List send()
    {
        run();
        return dist;
    }
    
    public static List Ultrasonic(String Output){
        List TempList = new ArrayList();
        Output = Output.substring(Output.indexOf("field1\":")+1);
        String[] res = Output.split("");
        for(int i=1;i<res.length;i++) {
            if(res[i].equals(",")) {
                continue;
            }
            else {
                try {
                    TempList.add(Integer.valueOf(res[i].substring(res[i].indexOf("field2\":")+1)));
                } catch (NumberFormatException e) {}
            }
        }

        return TempList;
    }
    
    public static List DHT(String Output){
        List TempList = new ArrayList();
        Output = Output.substring(Output.indexOf("field1\":")+1);
        String[] res = Output.split("");
        for(int i=1;i<res.length;i++) {
            if(res[i].equals(",")) {
                continue;
            }
            else {
                try {
                    TempList.add(Integer.valueOf(res[i].substring(res[i].indexOf("field2\":")+1)));
                } catch (NumberFormatException e) {}
            }
        }

        return TempList;
    }

   
    public static String getUrlContents(String theUrl){
        StringBuilder content = new StringBuilder();
        try
        {
            URL url = new URL(theUrl); // creating a url object
            URLConnection urlConnection = url.openConnection(); // creating a urlconnection object

            // wrapping the urlconnection in a bufferedreader
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            String line;
            // reading from the urlconnection using the bufferedreader
            while ((line = bufferedReader.readLine()) != null)
            {
                content.append(line + "\n");
            }
            bufferedReader.close();
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
        return content.toString();
    }
}
