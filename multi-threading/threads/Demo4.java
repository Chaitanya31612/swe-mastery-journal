public class Demo4 {
  public static void main(String[] args) {
    System.out.println("main thread");
    System.out.println(Thread.currentThread().getName());
    System.out.println(Thread.currentThread().getPriority());

    Thread t1 = new Thread(() -> {
      System.out.println("Name of 1st thread: " + Thread.currentThread().getName());
      System.out.println("Priority of 1st thread: " + Thread.currentThread().getPriority());
    });

    Thread t2 = new Thread(() -> {
      System.out.println("Name of 2nd thread: " + Thread.currentThread().getName());
      System.out.println("Priority of 2nd thread: " + Thread.currentThread().getPriority());
    });

    t1.start();
    t2.start();
  }
}
