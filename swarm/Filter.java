import java.io.*;
public class Filter {
public static void main(String[] args) throws IOException {
BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
String line;
boolean print = true;
while((line = in.readLine()) != null) {
if(print) System.out.println(line);
print = !print;
}
}
}
