public class Demo {
  public static void main(String[] args) {
    MyThread t1 = new MyThread();
    t1.start();
    /*
      t1.start() asks the JVM to run the run()
      method in a separate thread with its own
      call stack and program counter.
    */
  }
}

class MyThread extends Thread {
  @Override
  public void run() {
    System.out.println("My thread is running");
  }
}
