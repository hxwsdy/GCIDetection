from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

last_percent_reported = None

def sparse_tuple_from(sequences, dtype=np.double):
    """Create a sparse representention of x.
    Args:
        sequences: a list of lists of type dtype where each element is a sequence
    Returns:
        A tuple with (indices, values, shape)
    """
    indices = []
    values = []

    for n, seq in enumerate(sequences):
        indices.extend(zip([n]*len(seq), range(len(seq))))
        values.extend(seq)
        # indices.extend(zip([n] * seq, range(seq)))
        # values.append(seq)

    indices = np.asarray(indices, dtype=np.int64)
    values = np.asarray(values, dtype=dtype)
    shape = np.asarray([len(sequences), np.asarray(indices).max(0)[1]+1], dtype=np.int64)

    return indices, values, shape

def pad_sequences(sequences, maxlen=None, dtype=np.double,
                  padding='post', truncating='post', value=0.):
    '''Pads each sequence to the same length: the length of the longest
    sequence.
        If maxlen is provided, any sequence longer than maxlen is truncated to
        maxlen. Truncation happens off either the beginning or the end
        (default) of the sequence. Supports post-padding (default) and
        pre-padding.
        Args:
            sequences: list of lists where each element is a sequence
            maxlen: int, maximum length
            dtype: type to cast the resulting sequence.
            padding: 'pre' or 'post', pad either before or after each sequence.
            truncating: 'pre' or 'post', remove values from sequences larger
            than maxlen either in the beginning or in the end of the sequence
            value: float, value to pad the sequences to the desired value.
        Returns
            x: numpy array with dimensions (number_of_sequences, maxlen)
            lengths: numpy array with the original sequence lengths
    '''
    lengths = np.asarray([len(s) for s in sequences], dtype=np.int64)

    nb_samples = len(sequences)
    if maxlen is None:
        maxlen = np.max(lengths)

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    sample_shape = tuple()
    for s in sequences:
        if len(s) > 0:
            sample_shape = np.asarray(s).shape[1:]
            break

    x = (np.ones((nb_samples, maxlen) + sample_shape) * value).astype(dtype)
    for idx, s in enumerate(sequences):
        if len(s) == 0:
            continue  # empty list was found
        if truncating == 'pre':
            trunc = s[-maxlen:]
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" not understood' % truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample %s of sequence at position %s is different from expected shape %s' %
                             (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x, lengths

def tensor_to_array(tensor):
    if len(tensor.shape) < 1:
        return []
    array = []
    for i in range(0, tensor.shape[0], 1):
        if len(tensor.shape) == 1:
            sub_array = tensor[i]
        else :
            sub_array = tensor_to_array(tensor[i])
        array.append(sub_array)

    # if len(tensor.shape) ==1 :
    #     for i in range(0, tensor.shape[0], 1):
    #         sub_array = tensor[i]
    #         array.append(sub_array)
    # else :
    #     for i in range(0, tensor.shape[0], 1):
    #         sub_array = tensor_to_array(tensor[i])
    #         array.append(sub_array)

    return array

def transpose_dimension(list):
    result = []
    array = np.array(list)
    rows, cols = array.shape[0], array.shape[1]
    for j in range(0, cols):
        row = []
        for i in range(0, rows):
            row.append(array[i][j])
        result.append(row)
    return result