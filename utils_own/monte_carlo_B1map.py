
"""alpha_0 = np.linspace(0, 45, num=15) # np.array([25,35,45] )
results_monte_carlo = np.zeros((alpha_0.size,N_iterations))
for j in range(alpha_0.size):
    S_alpha = equation_B1(init['T1'] ,init['TR'],get_sequence_alpha(alpha_0[j] ) , S0)
    std = 0.2*np.max(S_alpha ) 
    mean = 1*np.max(S_alpha ) 
    noise =  std * np.random.randn(S_alpha.size,N_iterations) + mean

    for i in range(N_iterations):
        y_obs = S_alpha +noise[:,i]
        x_values =[ init['T1'] ,init['TR']]
        for k in range(len(y_obs)):
            x_values.append(y_obs[k] )
        pop, _ = curve_fit(function_B1_double,
                                x_values,
                                y_obs,
                                maxfev=600)
                                
        results_monte_carlo[j,i] = pop # , a = pop #
#plt.plot(get_sequence_alpha(results_monte_carlo).T)   
plt.plot(alpha_0, alpha_0, '-', label='Ground truth' )#
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1), '-', label='Mean' )#
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1)+np.std(results_monte_carlo,axis=1), label='m + std')
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1)-np.std(results_monte_carlo,axis=1), label='m - std')
plt.legend()
#plt.plot(get_sequence_alpha(alpha_0), results_monte_carlo)
plt.show()
"""
# alpha = np.arange(90)
# keys_sub = search_keys_sub(init)#

#plt.title('Sensitivity ratio DAM')
# plt.xlabel('alpha [°]')
# plt.ylabel('S(alpha)/S(2*alpha)')
#plt.plot(alpha, theorical_ratio)
# plt.show()
