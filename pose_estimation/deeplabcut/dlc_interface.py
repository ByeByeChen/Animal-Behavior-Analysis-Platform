import deeplabcut as dlc
import os

class DeepLabCutProcessor:
    def __init__(self, task, scorer):
        self.task = task
        self.scorer = scorer
        self.video_path = None
        self.path_config_file = None

    def train(self, video_path):
        self.video_path = video_path
        video = [video_path]
        net_type = "efficentnet-b6"
        augmenter_type = "default"

        self.path_config_file = dlc.create_new_project(self.task, self.scorer, video, copy_videos=True)
        
        # Training
        dlc.extract_frames(self.path_config_file, mode="automatic", userfeedback=False)
        dlc.create_training_dataset(self.path_config_file, net_type=net_type, augmenter_type=augmenter_type)
        dlc.train_network(self.path_config_file)
        print("Training completed.")
        return os.path.abspath(self.path_config_file)
        

    def inference(self, video_path):

        if not self.path_config_file:
            print("Please train the model first.")
            return
        
        video = [video_path]
    
        # result_path = 'uploads/'+filename+'efficentnet-b6.csv'

        # Inference
        dlc.analyze_videos(self.path_config_file, video, save_as_csv=True)
        dlc.create_labeled_video(self.path_config_file, video, save_frames=False)
        dlc.plot_trajectories(self.path_config_file, video)
        print("Inference completed.")
        return True
        
        

