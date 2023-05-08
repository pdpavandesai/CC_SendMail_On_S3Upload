# Topic: To write a program to monitor an S3 Uri. Whenever a user uploads data into the S3 storage, the program should capture the details. At the end of the day the program must send out an email to select users displaying the following information.

# a.S3 Uri 

# b.Object Name

# c.Object Size 

# d.Object type

# In addition to the above, the program should create a thumbnail and store it in a different uri in case the user uploads an image (.jpg/jpeg/png)

Steps Involved:

1.Created AWS account

2.Created two S3 Buckets

    a)Source bucket: mys3bucket1304 (Primary bucket where file is uploaded)

    b)Secondary bucket: mys3bucket1304-resized (Bucket where thumbnail file gets uploaded)

3.Created Policies which allows s3:GetObject & s3:PutObject

4.Lambda Function
