# Storage Systems: Block, File, Object & Why DBs Hate Video

---

## Mental Model: The Hard Drive, The Shared Folder & The Giant Warehouse

Not all storage is the same. There are 3 fundamental ways computers store data:

### 1. Block Storage (e.g., AWS EBS, Laptop SSD)
* **Analogy:** A raw, blank physical hard drive plugged directly into your motherboard.
* **How it works:** The computer writes raw sectors of bytes ($O(1)$ block update).
* **Superpower:** Blazing fast sub-millisecond speeds. Can update 4 bytes in the middle of a 100GB file.
* **Catch:** Can usually only be plugged into **one server at a time**.
* **Best For:** Databases (PostgreSQL data directories) and Operating System boot drives.

### 2. File Storage (e.g., AWS EFS, NFS, Office Network Drive)
* **Analogy:** A shared office network folder (`/shared/contracts/deal.pdf`).
* **How it works:** Has directories, folders, and standard files.
* **Superpower:** **Multi-Attach.** 50 different servers can mount the same folder and read/write files at the same time.
* **Catch:** Slower than raw block storage because of network file-sharing protocol overhead.
* **Best For:** Shared media assets for web content management systems (WordPress), legacy apps.

### 3. Object Storage (e.g., AWS S3, Google Cloud Storage)
* **Analogy:** A massive automated shipping warehouse.
* **How it works:** There are no "folders" or raw sectors. Everything is an **Object** with an ID key (`bucket/my-dog.jpg`), accessed via HTTP REST APIs (`GET /photo.jpg`).
* **Superpower:** **Virtually infinite scale and 11 9's of durability.** Amazon automatically replicates every file across 3 separate datacenters. It costs pennies per gigabyte.
* **Catch:** **Immutable.** You cannot change 1 word inside a 50MB PDF in S3; to change it, you must re-upload the whole 50MB file.
* **Best For:** Images, videos, PDF invoices, backups, log archives.

---

## The #1 Storage Rule: Never Put Pictures in Your SQL Database!

Why do senior engineers cringe when they see an image saved in a SQL `BLOB` column?

$$\mathbf{\text{Rule: Heavy binary files go to S3. Only the short URL string goes in the Database!}}$$

```
THE WRONG WAY (The Memory Choke):
[ User ] ---> [ Web App ] ---> Reads 20MB Video BLOB from Database
                               * Flushing 2,500 hot customer rows out of RAM!
                               * Database CPU and Network pipe choke!

THE RIGHT WAY (Direct Separation):
[ User ] ---> Database holds:  { "id": 101, "video_url": "https://s3.aws.com/v101.mp4" }
         ---> Direct stream:   Streams 20MB directly from S3 / CDN! (Database is untouched!)
```

---

## The Pre-Signed URL Trick: Why Your Web Servers Shouldn't Touch Files

Imagine you are ordering a new refrigerator:
* Do you tell the delivery truck to bring the refrigerator to your office desk, so you can carry it home in your trunk? **Of course not!**
* You give the delivery driver a gate code to deliver it **directly to your house**.

```
[ User Browser ] ----(1) "I want to upload a 500MB video" ----> [ Web Server ]
       |                                                               |
       | <---(2) "Here's a temporary 5-minute upload ticket" ----------+
       |         (S3 Pre-Signed URL)
       |
       +----(3) Uploads 500MB DIRECTLY to Amazon S3 -----------------> [ AWS S3 ]
                                                                           |
       <----(4) S3 confirms: "Uploaded successfully!" ---------------------+
       |
       +----(5) "Done! Save the S3 URL in my profile" ---------------> [ Web Server ]
```

* **Why this is genius:** Your application server's CPU, RAM, and network connections **never touch the 500MB file**! The app server only handles two tiny JSON messages (Step 1 and Step 5). Your servers can handle 100,000 users without breaking a sweat!

---

## Practice: Where Does It Live?

> **For each piece of data, choose where it belongs:**  
> `Relational Database`, `Object Storage (S3)`, `Block Storage (EBS)`, or `Cold Archive (Glacier)`.

1. **User Profile Avatar (2 MB JPEG):**
2. **User Password Hash & Email:**
3. **Database Write-Ahead Log (WAL) Files:**
4. **7 Years of Bank Transaction Audits (Legally required, but accessed once a year):**

---

## 60-Second Summary

> "Storage is a spectrum between speed, flexibility, and cost. Block storage gives sub-millisecond random I/O for database data files. File storage provides shared folder access across multiple servers. Object storage (S3) provides infinite, dirt-cheap, highly durable storage for immutable files like photos and videos. Never store binary media directly in relational databases; use the Pre-Signed URL pattern so users stream files directly to S3, leaving your web servers and databases fast and unburdened."
