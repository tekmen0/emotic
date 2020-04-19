import os 
import argparse

from train import train_emotic
from test import test_emotic

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default=0)
    parser.add_argument('--mode', type=str, default='train_test', choices=['train', 'test', 'train_test', 'inference'])
    parser.add_argument('--data_path', type=str, required=True, help='Path to preprocessed data npy files')
    parser.add_argument('--experiment_path', type=str, required=True, help='Path to save experiment files (results, models, logs)')
    parser.add_argument('--model_dir', type=str, default='models', help='Path to save models')
    parser.add_argument('--result_dir', type=str, default='results', help='Path to save results (prediction, labels mat file)')
    parser.add_argument('--log_dir', type=str, default='logs', help='Path to save logs (train, val)')
    parser.add_argument('--context_model', type=str, default='resnet18', choices=['resnet18', 'resnet50'])
    parser.add_argument('--body_model', type=str, default='resnet18', choices=['resnet18', 'resnet50'])
    parser.add_argument('--learning_rate', type=float, default=0.01)
    parser.add_argument('--weight_decay', type=float, default=5e-4)
    parser.add_argument('--cat_loss_weight', type=float, default=0.5)
    parser.add_argument('--cont_loss_weight', type=float, default=0.5)
    parser.add_argument('--continuous_loss_type', type=str, default='Smooth L1', choices=['L2', 'Smooth L1'])
    parser.add_argument('--discrete_loss_weight_type', type=str, default='dynamic', choices=['dynamic', 'mean', 'static'])
    parser.add_argument('--epochs', type=int, default=15)
    parser.add_argument('--batch_size', type=int, default=52) # use batch size = double(categorical emotion classes)
    # Generate args
    args = parser.parse_args()
    return args

''' Check (create if they don't exist) experiment directories '''
def check_paths(args):    
    folders= [args.result_dir, args.model_dir]
    paths = list()
    for folder in folders:
        folder_path = os.path.join(args.experiment_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        paths.append(folder_path)
        
    log_folders = ['train', 'val']
    for folder in log_folders:
        folder_path = os.path.join(args.experiment_path, args.log_dir, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        paths.append(folder_path)
    return paths


if __name__ == '__main__':
    args = parse_args()
    print ('mode ', args.mode)

    result_path, model_path, train_log_path, val_log_path = check_paths(args)

    cat = ['Affection', 'Anger', 'Annoyance', 'Anticipation', 'Aversion', 'Confidence', 'Disapproval', 'Disconnection', \
            'Disquietment', 'Doubt/Confusion', 'Embarrassment', 'Engagement', 'Esteem', 'Excitement', 'Fatigue', 'Fear','Happiness', \
            'Pain', 'Peace', 'Pleasure', 'Sadness', 'Sensitivity', 'Suffering', 'Surprise', 'Sympathy', 'Yearning']

    cat2ind = {}
    ind2cat = {}
    for idx, emotion in enumerate(cat):
        cat2ind[emotion] = idx
        ind2cat[idx] = emotion

    context_mean = [0.4690646, 0.4407227, 0.40508908]
    context_std = [0.2514227, 0.24312855, 0.24266963]
    body_mean = [0.43832874, 0.3964344, 0.3706214]
    body_std = [0.24784276, 0.23621225, 0.2323653]
    context_norm = [context_mean, context_std]
    body_norm = [body_mean, body_std]

    if args.mode == 'train':
        train_emotic(result_path, model_path, train_log_path, val_log_path, ind2cat, context_norm, body_norm, args)
    elif args.mode == 'test':
        test_emotic(result_path, model_path, ind2cat, context_norm, body_norm, args)
    elif args.mode == 'train_test':
        train_emotic(result_path, model_path, train_log_path, val_log_path, ind2cat, context_norm, body_norm, args)
        test_emotic(result_path, model_path, ind2cat, context_norm, body_norm, args)
    elif args.mode == 'inference':
        print ('not now')
    else:
        print ('Unknown mode')
    
