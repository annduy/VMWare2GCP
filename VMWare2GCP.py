import subprocess
import time

# Replace with your values###########
ovf_tool = 'C:\\Program Files\\VMware\\VMware OVF Tool\\ovftool.exe'
vmdk_path ='G:\\VMWare-VMs\\UbuntuServer20046'
vmx_file = 'UbuntuServer20046.vmx'
ova_file = "ubuntuserver20046.ova"
gcp_bucket = "20230906-1213"
gcp_instance_name = "ubuntuserver20046-vm-01"
gcp_zone = "asia-east1-b"
gcp_project = "wireguard-393804"
gcp_machine_type = "f1-micro"
############################################



# def show_progress(task):
#     print("Running subprocess: ", end="", flush=True)

#     # Define the interval for printing dots (e.g., one dot every second)
#     dot_interval = 1

#     # Track the start time
#     start_time = time.time()

#     # Loop to print dots while the subprocess is running
#     while True:
#         # Check if the subprocess has completed
#         return_code = task.poll()
#         if return_code is not None:
#             break

#         # Check the elapsed time
#         elapsed_time = time.time() - start_time

#         # Print a dot if the dot_interval has passed
#         if elapsed_time >= dot_interval:
#             print(".", end="", flush=True)
#             start_time = time.time()

#         # Optional: You can add a sleep to avoid high CPU usage
#         time.sleep(0.5)

#     # Ensure the subprocess completes and get its output
#     stdout, stderr = task.communicate()

#     # Print a newline to separate the dots from the subprocess output
#     print()

#     # Print the subprocess output
#     print("Subprocess Output:")
#     print(stdout)

#     # Print the subprocess error output (if any)
#     if stderr:
#         print("Subprocess Error Output:")
#         print(stderr)

#     # Check the return code of the subprocess
#     if task.returncode == 0:
#         print("Subprocess completed successfully.")
#     else:
#         print(f"Subprocess failed with return code {task.returncode}.")




# Convert VMWare VM to OVA
print("Converting VMware VM to OVA file")
task = subprocess.run( [f'{ovf_tool}', f'{vmdk_path}\{vmx_file}', f'{vmdk_path}\{ova_file}'], shell=True, check=True)
#show_progress(task)
print("OVA file was created")



# Upload the OVA file to GCP
upload_command = f"gsutil cp {vmdk_path}\{ova_file} gs://{gcp_bucket}/"
print("Uploading OVA file")
subprocess.run(upload_command, shell=True, check=True)
print("Uploading is completed")



#Create a GCP VM instance from the uploaded OVA
create_instance_command = f"gcloud compute instances import {gcp_instance_name} --project={gcp_project} --zone={gcp_zone}  --source-uri=gs://{gcp_bucket}/{ova_file} --machine-type={gcp_machine_type}"
subprocess.run(create_instance_command, shell=True, check=True)



###############
# Housekeeping 
###############
# delete OVA file on GCP's cloud storage
delete_gcp_ova_file_cmd = f"gsutil rm gs://{gcp_bucket}/{ova_file}"
print("deleting OVA file on GCP")
subprocess.run(delete_gcp_ova_file_cmd, shell=True, check=True)
print("OVA file on GCP was deleted")

# delete local OVA file
delete_local_ova_file_cmd = f"del {vmdk_path}\{ova_file}"
print("deleting local OVA file")
subprocess.run(delete_local_ova_file_cmd, shell=True, check=True)
print("local OVA file was deleted")

print("Your VM is on GCP now. Have fun with Google Cloud. :D")

