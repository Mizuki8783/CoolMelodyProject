from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ast
import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

pitch_symb = ['0',
 '49',
 '50',
 '51',
 '52',
 '53',
 '54',
 '55',
 '56',
 '57',
 '58',
 '59',
 '60',
 '61',
 '62',
 '63',
 '64',
 '65',
 '66',
 '67',
 '68',
 '69',
 '70',
 '71',
 '72',
 '73',
 '74',
 '75',
 '76',
 '77',
 '78',
 '79',
 '80',
 '81',
 '82',
 '83',
 '84',
 '85',
 '86',
 '87',
 '88',
 '89',
 '90',
 '91',
 '92']
duration_symb = ['1', '16', '16d', '2', '2d', '32', '32d', '4', '4d', '64', '8', '8d', '8dd']

L_pitch_symb = len(pitch_symb)
L_duration_symb = len(duration_symb)

len_in_64th_notes = {'64': 1, '32': 2, '32d': 3, '16': 4, '16d': 6, '8': 8, '8d': 12,
                     '8dd': 14, '4': 16, '4d': 24, '2': 32, '2d': 48, '1': 64}
duration_mapping = {1: 9,
 2: 5,
 3: 6,
 4: 1,
 6: 2,
 8: 10,
 12: 11,
 14: 12,
 16: 7,
 24: 8,
 32: 3,
 48: 4,
 64: 0}
pitch_mapping = {0: 0,
 49: 1,
 50: 2,
 51: 3,
 52: 4,
 53: 5,
 54: 6,
 55: 7,
 56: 8,
 57: 9,
 58: 10,
 59: 11,
 60: 12,
 61: 13,
 62: 14,
 63: 15,
 64: 16,
 65: 17,
 66: 18,
 67: 19,
 68: 20,
 69: 21,
 70: 22,
 71: 23,
 72: 24,
 73: 25,
 74: 26,
 75: 27,
 76: 28,
 77: 29,
 78: 30,
 79: 31,
 80: 32,
 81: 33,
 82: 34,
 83: 35,
 84: 36,
 85: 37,
 86: 38,
 87: 39,
 88: 40,
 89: 41,
 90: 42,
 91: 43,
 92: 44}

duration_reverse_mapping = {0: 64,
 1: 4,
 2: 6,
 3: 32,
 4: 48,
 5: 2,
 6: 3,
 7: 16,
 8: 24,
 9: 1,
 10: 8,
 11: 12,
 12: 14}
reverse_len_in_64th_notes = {v: k for k, v in len_in_64th_notes.items()}
pitch_reverse_mapping = {0: 0,
 1: 49,
 2: 50,
 3: 51,
 4: 52,
 5: 53,
 6: 54,
 7: 55,
 8: 56,
 9: 57,
 10: 58,
 11: 59,
 12: 60,
 13: 61,
 14: 62,
 15: 63,
 16: 64,
 17: 65,
 18: 66,
 19: 67,
 20: 68,
 21: 69,
 22: 70,
 23: 71,
 24: 72,
 25: 73,
 26: 74,
 27: 75,
 28: 76,
 29: 77,
 30: 78,
 31: 79,
 32: 80,
 33: 81,
 34: 82,
 35: 83,
 36: 84,
 37: 85,
 38: 86,
 39: 87,
 40: 88,
 41: 89,
 42: 90,
 43: 91,
 44: 92}

@app.get('/')
def greeting():
    return {'greeting':'you ding a big man ting bruv.'}

@app.get('/initialize')
def first_sequence():
    #-----generate data to randomly grab data from-----
    df_list = []
    for i in range(57):
        df = pd.read_csv(f'raw_data/clean_csvs/csv_{i}', sep='\t')
        df_list.append(df)

    random_value = random.randint(0,57)
    first_sequence = df_list[random_value]['pitch_dur0'][:8]

    #-----convert the first sequence to list of notes----
    lis_first_sequence = list(first_sequence)
    first_input_sequence = []
    for note in lis_first_sequence:
        note = note.split('-')
        note[0] = int(note[0])
        first_input_sequence.append(note)

    # #-----convert the sequence into the format model can take in-----
    # normalized_input_sequence = []
    # for note in before_normaliz_input_sequence:
    #     dur_len_in_64th_notes = len_in_64th_notes[str(note[1])]
    #     dur_mapped = duration_mapping[dur_len_in_64th_notes]
    #     pitch_mapped = pitch_mapping[note[0]]
    #     mapped_note = [pitch_mapped, dur_mapped]
    #     note_normalized = [mapped_note[0]/float(L_pitch_symb), mapped_note[1]/float(L_duration_symb)]
    #     normalized_input_sequence.append(note_normalized)

    # #-----grab the model and predict-----
    # model = keras.models.load_model("model/model.keras")


    # #-----take in the sequence and predict-----
    # input_sequence = np.array(normalized_input_sequence).reshape(1,8,2)
    # prediction = model.predict(input_sequence)

    # #-----transform the prediction into the notes the front-end can take in-----
    # # return predictions from sample
    # pitch_pred, duration_pred = prediction

    # # get log of predictions
    # pitch_pred = np.log(pitch_pred[0]) / 1.0  # diversity?
    # duration_pred = np.log(duration_pred[0])

    # # un-log predictions (not sure why we logged them...)
    # exp_pitch_preds = np.exp(pitch_pred)
    # exp_duration_preds = np.exp(duration_pred)

    # # make odds of all predictions = 1.0
    # pitch_pred = exp_pitch_preds / np.sum(exp_pitch_preds)
    # duration_pred = exp_duration_preds / np.sum(exp_duration_preds)

    # # get top 3 pitch predictions and top 2 duration predictions
    # pitch_index_top_3 = np.argpartition(pitch_pred, -3)[-3:]
    # dur_index_top_2 = np.argpartition(duration_pred, -2)[-2:]

    # # return three notes as [pitch, duration] pairs
    # three_notes = [[pitch, np.random.choice(dur_index_top_2)] for pitch in pitch_index_top_3]
    # three_notes_mapped = [[pitch_reverse_mapping[pitch], reverse_len_in_64th_notes[duration_reverse_mapping[duration]]] for pitch, duration in three_notes]

    return {'first_sequence': first_input_sequence} #before normalizing format

@app.get('/predict')
def predict(sequence):
    #-----grabbing the model-----
    model = keras.models.load_model("model/model.keras")

    #-----transform the sequence to the format model can take in-----
    #sequence example : [actual pitch, actual duration]
    list_sequence = ast.literal_eval(sequence)
    input_sequence = []

    for note in list_sequence:
        dur_len_in_64th_notes = len_in_64th_notes[str(note[1])]
        dur_mapped = duration_mapping[dur_len_in_64th_notes]
        pitch_mapped = pitch_mapping[note[0]]
        mapped_note = [pitch_mapped, dur_mapped]
        note_normalized = [mapped_note[0]/float(L_pitch_symb), mapped_note[1]/float(L_duration_symb)]
        input_sequence.append(note_normalized)

    #-----take in the sequence and predict-----
    input_sequence = np.array(input_sequence).reshape(1,8,2)
    prediction = model.predict(input_sequence)

    #-----transform the prediction into the notes the front-end can take in-----
    # return predictions from sample
    pitch_pred, duration_pred = prediction

    # get log of predictions
    pitch_pred = np.log(pitch_pred[0]) / 1.0  # diversity?
    duration_pred = np.log(duration_pred[0])

    # un-log predictions (not sure why we logged them...)
    exp_pitch_preds = np.exp(pitch_pred)
    exp_duration_preds = np.exp(duration_pred)

    # make odds of all predictions = 1.0
    pitch_pred = exp_pitch_preds / np.sum(exp_pitch_preds)
    duration_pred = exp_duration_preds / np.sum(exp_duration_preds)

    # get top 3 pitch predictions and top 2 duration predictions
    pitch_index_top_3 = np.argpartition(pitch_pred, -3)[-3:]
    dur_index_top_2 = np.argpartition(duration_pred, -2)[-2:]

    # return three notes as [pitch, duration] pairs
    three_notes = [[pitch, np.random.choice(dur_index_top_2)] for pitch in pitch_index_top_3]
    three_notes_mapped = [[pitch_reverse_mapping[pitch], reverse_len_in_64th_notes[duration_reverse_mapping[duration]]] for pitch, duration in three_notes]


    return {'predictions': three_notes_mapped}
