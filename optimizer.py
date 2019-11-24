from matplotlib import pyplot as plt
import skopt

import builder


calls = 10

altitude_space = skopt.space.Integer(low=1, high=200, name='altitude')

params = [altitude_space]



@skopt.utils.use_named_args(dimensions=params)
def strengthToWeight(altitude):

   stw = builder.build_struct(altitude)
   
   
   return stw


if __name__ == '__main__':
    res = skopt.gp_minimize(
        func=strengthToWeight,
        dimensions=params,
        acq_func='EI',
        n_calls=calls,
    )



    skopt.dump(res, 'result', store_objective=True)
    stw_min = skopt.expected_minimum(res, n_random_starts=20, random_state=None)
    print(stw_min)



    matplotlib.style.use('classic')

    fig1 = skopt.plots.plot_convergence(res)
    fig2, ax = skopt.plots.plot_objective(result=res, dimension_names=dims)
    fig3, ax = skopt.plots.plot_evaluations(result=res, dimension_names=dims)

    fig2.tight_layout()
    fig3.tight_layout()