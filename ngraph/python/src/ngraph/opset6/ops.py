# ******************************************************************************
# Copyright 2017-2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

"""Factory functions for all ngraph ops."""
from typing import Callable, Iterable, List, Optional, Set, Union

import numpy as np
from functools import partial

from ngraph.impl import Node, Shape
from ngraph.impl.op import Constant, Parameter
from ngraph.opset_utils import _get_node_factory
from ngraph.utils.decorators import binary_op, nameable_op, unary_op
from ngraph.utils.input_validation import (
    assert_list_of_ints,
    check_valid_attributes,
    is_non_negative_value,
    is_positive_value,
)
from ngraph.utils.node_factory import NodeFactory
from ngraph.utils.tensor_iterator_types import (
    GraphBody,
    TensorIteratorSliceInputDesc,
    TensorIteratorMergedInputDesc,
    TensorIteratorInvariantInputDesc,
    TensorIteratorBodyOutputDesc,
    TensorIteratorConcatOutputDesc,
)
from ngraph.utils.types import (
    NodeInput,
    NumericData,
    NumericType,
    ScalarData,
    TensorShape,
    as_node,
    as_nodes,
    get_dtype,
    get_element_type,
    get_element_type_str,
    make_constant_node,
)

_get_node_factory_opset6 = partial(_get_node_factory, "opset6")

# -------------------------------------------- ops ------------------------------------------------


@nameable_op
def ctc_greedy_decoder_seq_len(
        data: NodeInput,
        sequence_length: NodeInput,
        blank_index: Optional[NodeInput] = None,
        merge_repeated: bool = True,
        classes_index_type: str = "i32",
        sequence_length_type: str = "i32",
        name: Optional[str] = None,
) -> Node:
    """Return a node which performs CTCGreedyDecoderSeqLen.

    @param data:            The input 3D tensor. Shape: [batch_size, seq_length, num_classes]
    @param sequence_length: Input 1D tensor with sequence length. Shape: [batch_size]
    @param blank_index:     Scalar or 1D tensor with specifies the class index to use for the blank class.
                            Optional parameter. Default value is num_classes-1.
    @return:                The new node which performs CTCGreedyDecoderSeqLen.
    """
    if blank_index is not None:
        inputs = as_nodes(data, sequence_length, blank_index)
    else:
        inputs = as_nodes(data, sequence_length)

    attributes = {
        "merge_repeated": merge_repeated,
        "classes_index_type": classes_index_type,
        "sequence_length_type": sequence_length_type
    }

    return _get_node_factory_opset6().create("CTCGreedyDecoderSeqLen", inputs, attributes)


@nameable_op
def gather_elements(
    data: NodeInput,
    indices: NodeInput,
    axis: Optional[int] = 0,
    name: Optional[str] = None,
) -> Node:
    """Return a node which performs GatherND.

    @param data:       N-D tensor with data for gathering
    @param indices:    N-D tensor with indices by which data is gathered
    @param axis:       axis along which elements are gathered
    @return:           The new node which performs GatherElements
    """
    inputs = as_nodes(data, indices)

    attributes = {
        "axis": axis
    }

    return _get_node_factory_opset6().create("GatherElements", inputs, attributes)
