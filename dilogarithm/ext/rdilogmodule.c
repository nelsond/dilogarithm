#include <Python.h>
#include "math.h"
#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include "numpy/npy_3kcompat.h"

/* Docstring for the python function */

#define DOCSTRING \
"Calculates the Dilogarithm (Polylogarithm with order 2)  of all elements in\n\
the input array.\n\
\n\
Note: Input array must be real. The current implementation is fully adapted\n\
from the Fortran RDILOG function in CERNLIB (C332).\n\
\n\
Args:\n\
    x (array_like): input value\n\
\n\
Returns:\n\
  ndarray or scalar: Output array, element-wise dilogarithm of x.\n\
                     This is a scalar if x is a scalar."

static PyMethodDef DilogarithmMethods[] = {
        {NULL, NULL, 0, NULL}
};

/* The loop definition must precede the PyMODINIT_FUNC. */
double d_rdilog(double x);

static void double_rdilog(char **args, npy_intp *dimensions,
                          npy_intp* steps, void* data)
{
  npy_intp i;
  npy_intp n = dimensions[0];
  char *in = args[0], *out = args[1];
  npy_intp in_step = steps[0], out_step = steps[1];

  double tmp;

  for (i = 0; i < n; i++) {
    tmp = *(double *)in;
    *((double *)out) = d_rdilog(tmp);

    in += in_step;
    out += out_step;
  }
}

/*This a pointer to the above function*/
PyUFuncGenericFunction funcs[1] = {&double_rdilog};

/* These are the input and return dtypes of logit.*/
static char types[2] = {NPY_DOUBLE, NPY_DOUBLE};

static void *data[1] = {NULL};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "dilogarithm",
    NULL,
    -1,
    DilogarithmMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_dilogarithm(void)
{
  PyObject *m, *double_rdilog, *d;
  m = PyModule_Create(&moduledef);
  if (!m) {
    return NULL;
  }

  import_array();
  import_umath();

  double_rdilog = PyUFunc_FromFuncAndData(funcs, data, types, 1, 1, 1,
                                          PyUFunc_None, "rdilog",
                                          DOCSTRING, 0);

  d = PyModule_GetDict(m);

  PyDict_SetItemString(d, "rdilog", double_rdilog);
  Py_DECREF(double_rdilog);

  return m;
}

/* Dilogarithm for real valued arguments
 * Adapted from Fortran CERNLIB RDILOG function (C332)
 * See http://cernlib.web.cern.ch/cernlib/download/2006_source/src/mathlib/gen/c/dilog64.F
 *     http://cmd.inp.nsk.su/old/cmd2/manuals/cernlib/shortwrups/node64.html */

 const double HF = 0.5;
 const double PIsq = M_PI*M_PI;
 const double PI3 = PIsq/3;
 const double PI6 = PIsq/6;
 const double PI12 = PIsq/12;
 const double C[20] = {
   0.42996693560813697,
   0.40975987533077105,
   -0.01858843665014592,
   0.00145751084062268,
   -0.00014304184442340,
   0.00001588415541880,
   -0.00000190784959387,
   0.00000024195180854,
   -0.00000003193341274,
   0.00000000434545063,
   -0.00000000060578480,
   0.00000000008612098,
   -0.00000000001244332,
   0.00000000000182256,
   -0.00000000000027007,
   0.00000000000004042,
   -0.00000000000000610,
   0.00000000000000093,
   -0.00000000000000014,
   0.00000000000000002
 };

double d_rdilog(double x)
{
  double A, ALFA, B0, B1, B2, H, S, T, Y;

  if (x == 1) {
    H = PI6;
  } else if (x == -1) {
    H = -PI12;
  } else {
    T = -x;

    if (T <= -2) {
      Y = -1 / (1 + T);
      S = 1;
      A = -PI3 + HF * (pow(log(-T), 2) - pow(log(1 + 1/T), 2));
    } else if (T < -1) {
      Y = -1 - T;
      S = -1;
      A = log(-T);
      A = -PI6 + A * (A + log(1 + 1/T));
    } else if (T <= -0.5) {
      Y = -(1 + T) / T;
      S = 1;
      A = log(-T);
      A = -PI6 + A * (-HF * A + log(1 + T));
    } else if (T < 0) {
      Y = -T / (1 + T);
      S = -1;
      A = HF * pow(log(1 + T), 2);
    } else if (T <= 1) {
      Y = T;
      S = 1;
      A = 0;
    } else {
      Y = 1 / T;
      S = -1;
      A = PI6 + HF * pow(log(T), 2);
    }

    H = Y + Y - 1;
    ALFA = H + H;
    B1 = 0;
    B2 = 0;

    for (int i = 19; i >= 0; i--){
      B0 = C[i] + ALFA * B1 - B2;
      B2 = B1;
      B1 = B0;
    }

    H = -(S * (B0 - H * B2) + A);
  }

  return H;
}
