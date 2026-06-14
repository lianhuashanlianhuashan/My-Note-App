from flask import Flask, render_template, request,jsonify,send_file
import boto3
from datetime import datetime
import uuid
import io


app=Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/api/list-notes")
def list_note():
    s3=boto3.client('s3')
    response=s3.list_objects_v2(        #get all files in the notes/ folder
        Bucket="my-aws-s3-bucketaaaa",Prefix="notes/"
    )
    

    files=[]
    for item in response.get("Contents",[]):
        key=item["Key"]
        if key !="notes/":
            files.append(key)
    
    return jsonify({"files":files})


@app.route("/api/save-note", methods=['POST'])
def save_note():
    data=request.get_json()       #parse data send from frontend
    note=data.get('mynote')
    
    timestamp=datetime.now().strftime("%Y%m%d-%H%M%S")
    unique_id= uuid.uuid4()
    
    s3=boto3.client('s3')
    key = f"notes/{timestamp}--{unique_id}"
    s3.put_object(Bucket='my-aws-s3-bucketaaaa',Key= key,Body=note)
    return jsonify({"status":"success","message":"Note saved to cloud!"})
    
@app.route("/api/download-note", methods=["GET"])
def download_note():
    filekey=request.args.get("filekey")
    
    if not filekey:
        return {"error": "Missing key parameter"},400
    s3=boto3.client("s3")
    obj=s3.get_object(
        Bucket="my-aws-s3-bucketaaaa",Key=filekey
    )
    file_data=obj["Body"].read()
    
    return send_file(
        io.BytesIO(file_data),
        mimetype="text/plain",
        as_attachment=True,
        download_name=filekey.split("/")[-1]
    )

@app.route("/api/delete-note",methods=['DELETE'])
def delete_note():
    filekey=request.args.get("filekey")
    if not filekey:
        return {"error": "Missing key parameter"},400
    s3=boto3.client("s3")
    try:
        s3.delete_object(
            Bucket="my-aws-s3-bucketaaaa",
            Key=filekey
        )
        return {"meesage":"File deleted successfully", "filekey":filekey},200
    except Exception as e:
        return {"error": str(e)},500




if __name__=="__main__":
    app.run(debug=True, host ="0.0.0.0",port=8000 )
    