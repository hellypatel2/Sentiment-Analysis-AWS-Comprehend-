//https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-upload-object.html
import com.amazonaws.SdkClientException;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicSessionCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.*;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.services.s3.transfer.MultipleFileUpload;
import com.amazonaws.services.s3.transfer.TransferManager;
import com.amazonaws.services.s3.transfer.TransferManagerBuilder;
import com.amazonaws.services.s3.transfer.Upload;

import java.io.File;
import java.util.*;
import java.util.Arrays;
import java.io.File;


public class Fileupload {

    public static void main(String[] args) throws SdkClientException {

        String bucket = "sample-data-b00868907";
        String awsAccessKey="ASIATTT6YKKFRQH4WOEV";
        String awsSecretKey="0kWTJ9Ti3hSLudfEodPV1L0Y/WIAX8SHZPHT8yCl";
String sessionToken="FwoGZXIvYXdzEHsaDKz5vAgMbLYyGczXziK/ARdR63Y7jiDBpnPFWjbxoAe3J0BHH59QDzUSCqx5OWlFPmOGWXw9DgGje/X0GVLZ61MoozY9g2guyAdsqymoceRPZSj4gflTMVFfCBRF2+W2NLUhTcdmcik96KQhzgZ5b5z1kYwsBIOl4Q8CyRZxdW8MggIBZXdhazfMNSn27MBSsXsl2O0GCMONsFrWQcn5Yqq0j3HYC7OmQ6u/ja50s3Ejx9dk7Srm2mLkDrrzXvS9tkdm2m2u4Mu1MzFxf7PlKMPk24YGMi1GZtXAsG8vjP4DbI671c75fOqulxL0W8k3+WOwssLeAFp4jyTvcw36QkfaUoc=";
        BasicSessionCredentials sessionCredentials = new BasicSessionCredentials(awsAccessKey,awsSecretKey,sessionToken);

        AmazonS3 s3 = AmazonS3ClientBuilder.standard()
                .withCredentials(new AWSStaticCredentialsProvider(sessionCredentials))
                .withRegion(Regions.US_EAST_1)
                .build();

        TransferManager xfer_mgr = TransferManagerBuilder.standard().withS3Client(s3).build();
        File dir=new File("C:\\Users\\Helly\\Desktop\\dalhousie\\Serverless\\A3\\csci5410-assignment\\Assignment1\\Task2\\src\\main\\resources\\tech\\tech");

        List files=Arrays.asList(dir.listFiles());


        try {
            MultipleFileUpload xfer = xfer_mgr.uploadFileList(bucket,"" ,new File("."), files);
            XferMgrProgress.showTransferProgress(xfer);
            // or block with Transfer.waitForCompletion()
            XferMgrProgress.waitForCompletion(xfer);

        } catch (AmazonServiceException e) {
            System.err.println(e.getErrorMessage());
            System.exit(1);
        }
        xfer_mgr.shutdownNow();

   }
    }


