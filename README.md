## Conditional Trajectory Prediction project

### Data available: https://drive.google.com/drive/folders/1KVgkcLegHPaRc830pvqsbIEA3AClilOi?usp=sharing


### To train the MLP model on a GPU:
```
python lstm_train_test.py --end_epoch 120 --train_features ./features/forecasting_features_train.pkl --val_features ./features/forecasting_features_val.pkl --obs_len 20 --pred_len 30 --traj_save_path ./trajectories/lstm2/traj_val.pkl --joblib_batch_size 100 --gpu 0 --train_batch_size 512 --mlp --use_intersection
```

### To train the LSTM model on a GPU:
```
python lstm_train_test.py --end_epoch 120 --train_features ./features/forecasting_features_train.pkl --val_features ./features/forecasting_features_val.pkl --obs_len 20 --pred_len 30 --traj_save_path ./trajectories/lstm2/traj_val.pkl --joblib_batch_size 100 --gpu 0 --train_batch_size 512 --use_intersection
```