from typing import List, Tuple

import numpy as np

from gradman.context_graph import ContextGraph

"""Collection of all Tensor supported operations"""


def sum_(t: "Tensor") -> Tuple[np.ndarray, bool, List[ContextGraph]]:
    """Sum of elements of a Tensor

    Parameters
    ----------
    t : 'Tensor'
        t

    Returns
    -------
    Tuple[np.ndarray, bool, List[ContextGraph]]

    """
    o = t.data.sum()
    requires_grad = t.requires_grad

    if requires_grad:

        def grad_fn(grad: np.ndarray) -> np.ndarray:
            return grad * np.ones_like(t.data)

        _ctx = [ContextGraph(t, grad_fn)]
    else:
        _ctx = []

    return o, requires_grad, _ctx


def add_(t1: "Tensor", t2: "Tensor") -> Tuple[np.ndarray, bool, List[ContextGraph]]:
    """Addition of two tensors

    Parameters
    ----------
    t1 : "Tensor"
        t1
    t2 : 'Tensor'
        t2

    Returns
    -------
    Tuple[np.ndarray, bool, List[ContextGraph]]

    """

    o = t1.data + t2.data

    requires_grad = t1.requires_grad or t2.requires_grad
    _ctx: List[ContextGraph] = []

    if t1.requires_grad:

        def grad_fn1(grad: np.ndarray) -> np.ndarray:
            return grad

        _ctx.append(ContextGraph(t1, grad_fn1))

    if t2.requires_grad:

        def grad_fn2(grad: np.ndarray) -> np.ndarray:
            return grad

        _ctx.append(ContextGraph(t2, grad_fn2))

    return o, requires_grad, _ctx