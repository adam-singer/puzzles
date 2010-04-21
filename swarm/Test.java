public class Test {
public static void main(String[] args) {
if(args.length != 1) {
System.err.println("Usage: java Test <seed>");
System.exit(1);
}
java.util.Random r = new java.util.Random(Long.parseLong(args[0]));
int P = r.nextInt(999) + 1;
System.out.println(P);
while(P-- > 0) {
int T = r.nextInt(999) + 1;
int Z = r.nextInt(999) + 1;
System.out.println(T + " " + Z);
while(T-- > 0) {
int s = r.nextInt(999) + 1;
int m = (s + r.nextInt(100)) / 2;
System.out.println(s + " " + m);
}
}
}
}
