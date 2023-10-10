import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.notebook import tqdm
from pathlib import Path
import requests

def run_script():
    def run_cmd(cmd):
        process = subprocess.run(cmd, shell=True, check=True, text=True)
        return process.stdout

    # Change the current directory to /content/
    os.chdir('/content/')
    print("Changing dir to /content/")

    # Your function to edit the file
    def edit_file(file_path):
        temp_file_path = "/tmp/temp_file.py"
        changes_made = False
        with open(file_path, "r") as file, open(temp_file_path, "w") as temp_file:
            previous_line = ""
            second_previous_line = ""
            for line in file:
                new_line = line.replace("value=160", "value=128")
                if new_line != line:
                    print("Replaced 'value=160' with 'value=128'")
                    changes_made = True
                line = new_line

                new_line = line.replace("crepe hop length: 160", "crepe hop length: 128")
                if new_line != line:
                    print("Replaced 'crepe hop length: 160' with 'crepe hop length: 128'")
                    changes_made = True
                line = new_line

                new_line = line.replace("value=0.88", "value=0.75")
                if new_line != line:
                    print("Replaced 'value=0.88' with 'value=0.75'")
                    changes_made = True
                line = new_line

                if "label=i18n(\"输入源音量包络替换输出音量包络融合比例，越靠近1越使用输出包络\")" in previous_line and "value=1," in line:
                    new_line = line.replace("value=1,", "value=0.25,")
                    if new_line != line:
                        print("Replaced 'value=1,' with 'value=0.25,' based on the condition")
                        changes_made = True
                    line = new_line

                if "label=i18n(\"总训练轮数total_epoch\")" in previous_line and "value=20," in line:
                    new_line = line.replace("value=20,", "value=500,")
                    if new_line != line:
                        print("Replaced 'value=20,' with 'value=500,' based on the condition for DEFAULT EPOCH")
                        changes_made = True
                    line = new_line

                if 'choices=["pm", "harvest", "dio", "crepe", "crepe-tiny", "mangio-crepe", "mangio-crepe-tiny"], # Fork Feature. Add Crepe-Tiny' in previous_line:
                    if 'value="pm",' in line:
                        new_line = line.replace('value="pm",', 'value="mangio-crepe",')
                        if new_line != line:
                            print("Replaced 'value=\"pm\",' with 'value=\"mangio-crepe\",' based on the condition")
                            changes_made = True
                        line = new_line

                # Change Sample Rate by 48k
                if 'value="40k",' in line:
                    new_line = line.replace('value="40k",', 'value="48k",')
                    if new_line != line:
                        print("Replaced 'value=\"40k\",' with 'value=\"48k\",' based on the DEFAULT SAMPLE RATE !")
                        changes_made = true
                    line = new_line

                # Change Version by V2
                if 'value="v1",' in line:
                    new_line = line.replace('value="v1",', 'value="v2",')
                    if new_line != line:
                        print("Replaced 'value=\"v1\",' with value=\"v2\",' based on the DEFAULT VERSION !")
                        changes_made = True
                    line = new_line

                # Change Maximum Max Batch Size
                if "maximum=40," in line:
                    new_line = line.replace("maximum=40,", "maximum=80,")
                    if new_line != line:
                        print("Replaced 'maximum=40,' with 'maximum=80,' based on the MAX BATCH SIZE !")
                        changes_made = True
                    line = new_line

                # Change Maximum Save Every Epoch
                if "maximum=50," in line:
                    new_line = line.replace("maximum=50,", "maximum=1000,")
                    if new_line != line:
                        print("Replaced 'maximum=50,' with 'maximum=1000,' based on the SAVE EVERY EPOCH !")
                        changes_made = True
                    line = new_line

                # Change pretrained v2 path G
                if 'value="pretrained/f0G40k.pth",' in line:
                    new_line = line.replace('value="pretrained/f0G40k.pth",','value="pretrained_v2/f0G48k.pth",')
                    if new_line != line:
                        print("Replaced 'value=\"pretrained/f0G40k.pth\"' with 'value=\"pretrained_v2/f0G48k.pth\"' based on the G Path")
                        changes_made = True
                    line = new_line

                # Change pretrained v2 path D
                if 'value="pretrained/f0D40k.pth",' in line:
                    new_line = line.replace('value="pretrained/f0D40k.pth",','value="pretrained_v2/f0D48k.pth",')
                    if new_line != line:
                        print("Replaced 'value=\"pretrained/f0D40k.pth\"' with 'value=\"pretrained_v2/f0D48k.pth\"' based on the D Path")
                        changes_made = True
                    line = new_line

                # Check Cache all Training
                if 'label="Cache all training sets to GPU memory. Caching small datasets (less than 10 minutes) can speed up training, but caching large datasets will consume a lot of GPU memory and may not provide much speed improvement",' in previous_line:
                    if 'value=False,' in line:
                        new_line = line.replace('value=False,','value=True,')
                        if new_line != line:
                            print("Replaced 'value=False,' with 'value=True,' based on the Cache All Training")
                            changes_made = True
                        line = new_line

                # Change dataset path
                if 'value="/content/Retrieval-based-Voice-Conversion-WebUI\\\\datasets\\\\"' in line:
                    new_line = line.replace('value="/content/Retrieval-based-Voice-Conversion-WebUI\\\\datasets\\\\"', 'value="/content/dataset/"')
                    if new_line != line:
                        print("Replaced 'value=\"/content/Retrieval-based-Voice-Conversion-WebUI\\\\datasets\\\\\" with 'value=\"/content/dataset/\"' based on the dataset path")
                        changes_made = True
                    line = new_line
                
                

                new_line = line.replace('label=i18n("输入训练文件夹路径"), value="E:\\\\语音音频+标注\\\\米津玄师\\\\src"', 'label=i18n("输入训练文件夹路径"), value="/content/dataset/"')
                if new_line != line:
                    print("Replaced 'label=i18n(\"输入训练文件夹路径\"), value=\"E:\\\\语音音频+标注\\\\米津玄师\\\\src\"' with 'label=i18n(\"输入训练文件夹路径\"), value=\"/content/dataset/\"'")
                    changes_made = True
                line = new_line

                if 'label=i18n("是否仅保存最新的ckpt文件以节省硬盘空间"),' in second_previous_line:
                    if 'value=i18n("否"),' in line:
                        new_line = line.replace('value=i18n("否"),', 'value=i18n("是"),')
                        if new_line != line:
                            print("Replaced 'value=i18n(\"否\"),' with 'value=i18n(\"是\"),' based on the condition for SAVE ONLY LATEST")
                            changes_made = True
                        line = new_line

                if 'label=i18n("是否在每次保存时间点将最终小模型保存至weights文件夹"),' in second_previous_line:
                    if 'value=i18n("否"),' in line:
                        new_line = line.replace('value=i18n("否"),', 'value=i18n("是"),')
                        if new_line != line:
                            print("Replaced 'value=i18n(\"否\"),' with 'value=i18n(\"是\"),' based on the condition for SAVE SMALL WEIGHTS")
                            changes_made = True
                        line = new_line

                temp_file.write(line)
                second_previous_line = previous_line
                previous_line = line

        # After finished, we replace the original file with the temp one
        import shutil
        shutil.move(temp_file_path, file_path)

        if changes_made:
            print("Changes made and file saved successfully.")
        else:
            print("No changes were needed.")

    # Define the repo path
    repo_path = '/content/Retrieval-based-Voice-Conversion-WebUI'

    def copy_all_files_in_directory(src_dir, dest_dir):
        # Iterate over all files in source directory
        for item in Path(src_dir).glob('*'):
            if item.is_file():
                # Copy each file to destination directory
                shutil.copy(item, dest_dir)
            else:
                # If it's a directory, make a new directory in the destination and copy the files recursively
                new_dest = Path(dest_dir) / item.name
                new_dest.mkdir(exist_ok=True)
                copy_all_files_in_directory(str(item), str(new_dest))

    def clone_and_copy_repo(repo_path):
        # New repository link
        new_repo_link = "https://github.com/kalomaze/Mangio-Kalo-Tweaks.git"
        # Temporary path to clone the repository
        temp_repo_path = "/content/temp_Mangio-RVC-Fork"
        # New folder name
        new_folder_name = "Mangio-RVC-Fork"

        # Clone the latest code from the new repository to a temporary location
        run_cmd(f"git clone {new_repo_link} {temp_repo_path}")
        os.chdir(temp_repo_path)

        run_cmd("git checkout bf0ffdbc35da09b57306e429c6deda84496948a1")

        run_cmd("wget https://github.com/kalomaze/Mangio-Kalo-Tweaks/raw/patch-1/EasierGUI.py")

        # Edit the file here, before copying
        edit_file(f"{temp_repo_path}/infer-web.py")

        # Copy all files from the cloned repository to the existing path
        copy_all_files_in_directory(temp_repo_path, repo_path)
        print(f"Copying all {new_folder_name} files from GitHub.")

        # Change working directory back to /content/
        os.chdir('/content/')
        print("Changed path back to /content/")
        
        # Remove the temporary cloned repository
        shutil.rmtree(temp_repo_path)

    # Call the function
    clone_and_copy_repo(repo_path)

    # Download the credentials file for RVC archive sheet
    os.makedirs('/content/Retrieval-based-Voice-Conversion-WebUI/stats/', exist_ok=True)
    run_cmd("wget -q https://cdn.discordapp.com/attachments/945486970883285045/1114717554481569802/peppy-generator-388800-07722f17a188.json -O /content/Retrieval-based-Voice-Conversion-WebUI/stats/peppy-generator-388800-07722f17a188.json")

    # Forcefully delete any existing torchcrepe dependencies downloaded from an earlier run just in case
    shutil.rmtree('/content/Retrieval-based-Voice-Conversion-WebUI/torchcrepe', ignore_errors=True)
    shutil.rmtree('/content/torchcrepe', ignore_errors=True)

    # Download the torchcrepe folder from the maxrmorrison/torchcrepe repository
    run_cmd("git clone https://github.com/maxrmorrison/torchcrepe.git")
    shutil.move('/content/torchcrepe/torchcrepe', '/content/Retrieval-based-Voice-Conversion-WebUI/')
    shutil.rmtree('/content/torchcrepe', ignore_errors=True)  # Delete the torchcrepe repository folder

    # Change the current directory to /content/Retrieval-based-Voice-Conversion-WebUI
    os.chdir('/content/Retrieval-based-Voice-Conversion-WebUI')
    os.makedirs('pretrained', exist_ok=True)
    os.makedirs('uvr5_weights', exist_ok=True)

def download_file(url, filepath):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def download_pretrained_models():
    pretrained_models = {
        "pretrained": [
            "D40k.pth",
            "G40k.pth",
            "f0D40k.pth",
            "f0G40k.pth"
        ],
        "pretrained_v2": [
            "D40k.pth",
            "G40k.pth",
            "f0D40k.pth",
            "f0G40k.pth",
            "f0G48k.pth",
            "f0D48k.pth"
        ],
        "uvr5_weights": [
            "HP2-人声vocals+非人声instrumentals.pth",
            "HP5-主旋律人声vocals+其他instrumentals.pth"
        ]
    }

    base_url = "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/"
    base_path = "/content/Retrieval-based-Voice-Conversion-WebUI/"

    # Calculate total number of files to download
    total_files = sum(len(files) for files in pretrained_models.values()) + 1  # +1 for hubert_base.pt

    with tqdm(total=total_files, desc="Downloading files") as pbar:
        for folder, models in pretrained_models.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for model in models:
                url = base_url + folder + "/" + model
                filepath = os.path.join(folder_path, model)
                download_file(url, filepath)
                pbar.update()

        # Download hubert_base.pt to the base path
        hubert_url = base_url + "hubert_base.pt"
        hubert_filepath = os.path.join(base_path, "hubert_base.pt")
        download_file(hubert_url, hubert_filepath)
        pbar.update()

def clone_repository(run_download):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_script)
        if run_download:
            executor.submit(download_pretrained_models)
