""" Riemann zeta and related function. """
from sympy.core import Function, S, C, sympify, pi
from sympy.core.function import ArgumentIndexError

###############################################################################
###################### LERCH TRANSCENDENT #####################################
###############################################################################

class lerchphi(Function):
    r"""
    Lerch transcendent (Lerch phi function).

    For :math:`Re(a) > 0`, :math:`|z| < 1` and :math:`s \in \mathbb{C}`, the
    Lerch transcendent is defined as

    .. math :: \Phi(z, s, a) = \sum_{n=0}^\infty \frac{z^n}{(n + a)^s},

    where the standard branch of the argument is used for :math:`n + a`,
    and by analytic continuation for other values of the parameters.

    A commonly used related function is the Lerch zeta function, defined by

    .. math:: L(q, s, a) = \Phi(e^{2\pi i q}, s, a).

    **Analytic Continuation and Branching Behavior**

    It can be shown that

    .. math:: \Phi(z, s, a) = z\Phi(z, s, a+1) + a^{-s}.

    This provides the analytic continuation to :math:`Re(a) \le 0`.

    Assume now :math:`Re(a) > 0`. The integral representation

    .. math:: \Phi_0(z, s, a) = \int_0^\infty \frac{t^{s-1} e^{-at}}{1 - ze^{-t}}
                                \frac{\mathrm{d}t}{\Gamma(s)}

    provides an analytic continuation to :math:`\mathbb{C} - [1, \infty)`.
    Finally, for :math:`x \in (1, \infty)` we find

    .. math:: \lim_{\epsilon \to 0^+} \Phi_0(x + i\epsilon, s, a)
             -\lim_{\epsilon \to 0^+} \Phi_0(x - i\epsilon, s, a)
             = \frac{2\pi i \log^{s-1}{x}}{x^a \Gamma(s)},

    using the standard branch for both :math:`\log{x}` and
    :math:`\log{\log{x}}` (a branch of :math:`\log{\log{x}}` is needed to
    evaluate :math:`\log{x}^{s-1}`).
    This concludes the analytic continuation. The Lerch transcendent is thus
    branched at :math:`z \in \{0, 1, \infty\}` and
    :math:`a \in \mathbb{Z}_{\le 0}`. For fixed :math:`z, a` outside these
    branch points, it is an entire function of :math:`s`.

    See Also
    ========

    polylog, zeta

    References
    ==========

    - Bateman, H.; Erdelyi, A. (1953), Higher Transcendental Functions,
      Vol. I, New York: McGraw-Hill. Section 1.11.
    - http://dlmf.nist.gov/25.14
    - http://en.wikipedia.org/wiki/Lerch_transcendent

    Examples
    ========

    The Lerch transcendent is a fairly general function, for this reason it does
    not automatically evaluate to simpler functions. Use expand_func() to
    achieve this.

    If :math:`z=1`, the Lerch transcendent reduces to the Hurwitz zeta function:

    >>> from sympy import lerchphi, expand_func
    >>> from sympy.abc import z, s, a
    >>> expand_func(lerchphi(1, s, a))
    zeta(s, a)

    If :math:`a=1`, the Lerch transcendent reduces to the polylogarithm:

    >>> expand_func(lerchphi(z, s, 1))
    polylog(s, z)/z

    The derivatives with respect to :math:`z` and :math:`a` can be computed in
    closed form:

    >>> lerchphi(z, s, a).diff(z)
    (-a*lerchphi(z, s, a) + lerchphi(z, s - 1, a))/z
    >>> lerchphi(z, s, a).diff(a)
    -s*lerchphi(z, s + 1, a)
    """

    nargs = 3

    def _eval_expand_func(self, **hints):
        # TODO much more possible here
        if hints.get('deep', False):
            z, s, a = map(lambda x: x._eval_expand_func(**hints), self.args)
        else:
            z, s, a = self.args
        if z == 1:
            return zeta(s, a)
        if a == 1:
            return polylog(s, z)/z
        return lerchphi(z, s, a)

    def fdiff(self, argindex=1):
        z, s, a = self.args
        if argindex == 3:
            return -s*lerchphi(z, s+1, a)
        elif argindex == 1:
            return (lerchphi(z, s-1, a) - a*lerchphi(z, s, a))/z
        else:
            raise ArgumentIndexError

###############################################################################
###################### POLYLOGARITHM ##########################################
###############################################################################

class polylog(Function):
    r"""
    Polylogarithm function.

    For :math:`|z| < 1` and :math:`s \in \mathbb{C}`, the polylogarithm is
    defined by

    .. math:: \operatorname{Li}_s(z) = \sum_{n=1}^\infty \frac{z^n}{n^s},

    where the standard branch of the argument is used for :math:`n`. It admits
    an analytic continuation which is branched at :math:`z=1` (notably not on the
    sheet of initial definition), :math:`z=0` and :math:`z=\infty`.

    The name polylogarithm comes from the fact that for :math:`s=1`, the
    polylogarithm is related to the ordinary logarithm (see examples), and that

    .. math:: \operatorname{Li}_{s+1}(z) =
                    \int_0^z \frac{\operatorname{Li}_s(t)}{t} \mathrm{d}t.

    The polylogarithm is a special case of the Lerch transcendent:

    .. math:: \operatorname{Li}_{s}(z) = z \Phi(z, s, 1)

    See Also
    ========

    zeta, lerchphi

    Examples
    ========

    For :math:`z \in \{0, 1, -1\}`, the polylogarithm is automatically expressed
    using other functions:

    >>> from sympy import polylog
    >>> from sympy.abc import s
    >>> polylog(s, 0)
    0
    >>> polylog(s, 1)
    zeta(s)
    >>> polylog(s, -1)
    dirichlet_eta(s)

    If :math:`s` is a negative integer, :math:`0` or :math:`1`, the
    polylogarithm can be expressed using elementary functions. This can be
    done using expand_func():

    >>> from sympy import expand_func
    >>> from sympy.abc import z
    >>> expand_func(polylog(1, z))
    -log(-z + 1)
    >>> expand_func(polylog(0, z))
    z/(-z + 1)

    The derivative with respect to :math:`z` can be computed in closed form:

    >>> polylog(s, z).diff(z)
    polylog(s - 1, z)/z

    The polylogarithm can be expressed in terms of the lerch transcendent:

    >>> from sympy import lerchphi
    >>> polylog(s, z).rewrite(lerchphi)
    z*lerchphi(z, s, 1)
    """

    nargs = 2

    @classmethod
    def eval(cls, s, z):
        if z == 1:
            return zeta(s)
        elif z == -1:
            return dirichlet_eta(s)
        elif z == 0:
            return 0

    def fdiff(self, argindex=1):
        s, z = self.args
        if argindex == 2:
            return polylog(s-1, z)/z
        raise ArgumentIndexError

    def _eval_rewrite_as_lerchphi(self, s, z):
        return z*lerchphi(z, s, 1)

    def _eval_expand_func(self, **hints):
        from sympy import log, expand_mul, Dummy
        if hints.get('deep', False):
            s, z = map(lambda x: x._eval_expand_func(**hints), self.args)
        else:
            s, z = self.args
        if s == 1:
            return -log(1 - z)
        if s.is_Integer and s <= 0:
            u = Dummy('u')
            start = u/(1 - u)
            for _ in range(-s):
                start = u*start.diff(u)
            return expand_mul(start).subs(u, z)
        return polylog(s, z)

###############################################################################
###################### HURWITZ GENERALIZED ZETA FUNCTION ######################
###############################################################################

class zeta(Function):
    r"""
    Hurwitz zeta function (or Riemann zeta function).

    For :math:`Re(a) > 0` and :math:`Re(s) > 1`, this function is defined as

    .. math:: \zeta(s, a) = \sum_{n=0}^\infty \frac{1}{(n + a)^s},

    where the standard choice of argument for :math:`n + a` is used. For fixed
    :math:`a` with :math:`Re(a) > 0` the Hurwitz zeta function admits a
    meromorphic continuation to all of :math:`\mathbb{C}`, it is an unbranched
    function with a simple pole at :math:`s = 1`.

    Analytic continuation to other :math:`a` is possible under some circumstances,
    but this is not typically done.

    The Hurwitz zeta function is a special case of the Lerch transcendent:

    .. math:: \zeta(s, a) = \Phi(1, s, a).

    This formula defines an analytic continuation for all possible values of
    :math:`s` and :math:`a` (also :math:`Re(a) < 0`), see the documentation of
    :class:`lerchphi` for a description of the branching behavior.

    If no value is passed for :math:`a`, by this function assumes a default value
    of :math:`a = 1`, yielding the Riemann zeta function.

    See Also
    ========

    dirichlet_eta, lerchphi, polylog

    References
    ==========

    - http://dlmf.nist.gov/25.11
    - http://en.wikipedia.org/wiki/Hurwitz_zeta_function

    Examples
    ========

    For :math:`a = 1` the Hurwitz zeta function reduces to the famous Riemann
    zeta function:

    .. math:: \zeta(s, 1) = \zeta(s) = \sum_{n=1}^\infty \frac{1}{n^s}.

    >>> from sympy import zeta
    >>> from sympy.abc import s
    >>> zeta(s, 1)
    zeta(s)

    The Riemann zeta function can also be expressed using the Dirichlet eta
    function:

    >>> from sympy import dirichlet_eta
    >>> zeta(s).rewrite(dirichlet_eta)
    dirichlet_eta(s)/(-2**(-s + 1) + 1)

    The Riemann zeta function at positive even integer and negative odd integer
    values is related to the Bernoulli numbers:

    >>> zeta(2)
    pi**2/6
    >>> zeta(4)
    pi**4/90
    >>> zeta(-1)
    -1/12

    The specific formulae are:

    .. math:: \zeta(2n) = (-1)^{n+1} \frac{B_{2n} (2\pi)^{2n}}{2(2n)!}
    .. math:: \zeta(-n) = -\frac{B_{n+1}}{n+1}

    At negative even integers the Riemann zeta function is zero:

    >>> zeta(-4)
    0

    No closed-form expressions are known at positive odd integers, but
    numerical evaluation is possible:

    >>> zeta(3).n()
    1.20205690315959

    The derivative of :math:`\zeta(s, a)` with respect to :math:`a` is easily
    computed:

    >>> from sympy.abc import a
    >>> zeta(s, a).diff(a)
    -s*zeta(s + 1, a)

    However the derivative with respect to :math:`s` has no useful closed form
    expression:

    >>> zeta(s, a).diff(s)
    Derivative(zeta(s, a), s)

    The Hurwitz zeta function can be expressed in terms of the Lerch transcendent,
    :class:`sympy.functions.special.lerchphi`:

    >>> from sympy import lerchphi
    >>> zeta(s, a).rewrite(lerchphi)
    lerchphi(1, s, a)

    """

    nargs = (1, 2)

    @classmethod
    def eval(cls, z, a_=None):
        if a_ is None:
            z, a = map(sympify, (z, 1))
        else:
            z, a = map(sympify, (z, a_))

        if a.is_Number:
            if a is S.NaN:
                return S.NaN
            elif a is S.One and a_ is not None:
                return cls(z)
            # TODO Should a == 0 return S.NaN as well?

        if z.is_Number:
            if z is S.NaN:
                return S.NaN
            elif z is S.Infinity:
                return S.One
            elif z is S.Zero:
                if a.is_negative:
                    return S.Half - a - 1
                else:
                    return S.Half - a
            elif z is S.One:
                return S.ComplexInfinity
            elif z.is_Integer:
                if a.is_Integer:
                    if z.is_negative:
                        zeta = (-1)**z * C.bernoulli(-z+1)/(-z+1)
                    elif z.is_even:
                        B, F = C.bernoulli(z), C.factorial(z)
                        zeta = 2**(z-1) * abs(B) * pi**z / F
                    else:
                        return

                    if a.is_negative:
                        return zeta + C.harmonic(abs(a), z)
                    else:
                        return zeta - C.harmonic(a-1, z)

    def _eval_rewrite_as_dirichlet_eta(self, s, a=1):
        if a != 1:
            return self
        s = self.args[0]
        return dirichlet_eta(s)/(1 - 2**(1 - s))

    def _eval_rewrite_as_lerchphi(self, s, a=1):
        return lerchphi(1, s, a)

    def fdiff(self, argindex=1):
        if len(self.args) == 2:
            s, a = self.args
        else:
            s, a = self.args + (1,)
        if argindex == 2:
            return -s*zeta(s + 1, a)
        else:
            raise ArgumentIndexError

class dirichlet_eta(Function):
    r"""
    Dirichlet eta function.

    For :math:`Re(s) > 0`, this function is defined as

    .. math:: \eta(s) = \sum_{n=1}^\infty \frac{(-1)^n}{n^s}.

    It admits a unique analytic continuation to all of :math:`\mathbb{C}`.
    It is an entire, unbranched function.

    See Also
    ========

    zeta

    References
    ==========

    - http://en.wikipedia.org/wiki/Dirichlet_eta_function

    Examples
    ========

    The Dirichlet eta function is closely related to the Riemann zeta function:

    >>> from sympy import dirichlet_eta, zeta
    >>> from sympy.abc import s
    >>> dirichlet_eta(s).rewrite(zeta)
    (-2**(-s + 1) + 1)*zeta(s)

    """
    nargs = 1

    @classmethod
    def eval(cls, s):
        if s == 1:
            return C.log(2)
        z = zeta(s)
        if not z.has(zeta):
            return (1-2**(1-s))*z

    def _eval_rewrite_as_zeta(self, s):
        return (1-2**(1-s)) * zeta(s)
