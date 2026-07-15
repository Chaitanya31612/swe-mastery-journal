public class Demo3 {
  public static void main(String[] args) {
    Thread thread = new Thread(() -> System.out.println("My thread is running"));
    thread.start();
  }
}
