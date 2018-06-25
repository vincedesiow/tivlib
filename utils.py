import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def show_pnl(direction, out_sample_price, save=False,
			 text_path=None, fig_path=None):
	direction = np.array(direction)
	daily_profits = (direction[:-1] * (out_sample_price[1:].values - out_sample_price[:-1].values))
	cumulative_profits = np.cumsum(daily_profits)
	if not save:
		print("Total profit after %i trading days since %s: %f"%(len(cumulative_profits), out_sample_price.index[0], cumulative_profits[-1]))
		print("Average daily profit: ", daily_profits.mean())
		print("Sharpe: ", daily_profits.mean()/daily_profits.std())
		print("Times change in direction: ", np.count_nonzero(direction[1:] - direction[:-1]))
		day_zero_price = out_sample_price[-len(cumulative_profits)]
		print("Annualized returns based on 252 trading days per year and investing in 1 unit of iron on day 0: ", 
			 round(((sum(daily_profits) + day_zero_price)/day_zero_price) ** (252/len(cumulative_profits)) - 1, 5) * 100, "%")
		print_dir = "long" if direction[-1] > 0 else "short"
		print("Direction to take now: " + print_dir)
		fig, ax = plt.subplots(1,2, figsize=(18,6))

		ax[0].hist(daily_profits)
		ax[0].set_title("Distribution of Daily Profits")
		ax[0].set_xlabel("Profits")
		ax[0].set_ylabel("Number of Days")
		ax[1].plot(np.arange(len(cumulative_profits)), cumulative_profits, label="Cumulative Profits")
		ax[1].plot(np.arange(len(cumulative_profits)), 
				   out_sample_price[-len(cumulative_profits):] - out_sample_price[-len(cumulative_profits)], 
				   label="Long Asset Only")
		ax[1].set_title("Cumulative Daily Profits")
		ax[1].set_xlabel("Day")
		ax[1].set_ylabel("Cumulative PNL")
		plt.legend()
		plt.show()
	else:
		f = open(text_path, "w+")
		f.write("Total profit after %i trading days since %s: %f\n"%(len(cumulative_profits), out_sample_price.index[0], cumulative_profits[-1]))
		f.write("Average daily profit: %f\n"%(daily_profits.mean()))
		f.write("Sharpe: %f\n"%(daily_profits.mean()/daily_profits.std()))
		f.write("Times change in direction: %i\n"%(np.count_nonzero(direction[1:] - direction[:-1])))
		day_zero_price = out_sample_price[-len(cumulative_profits)]
		returns = round(((sum(daily_profits) + day_zero_price)/day_zero_price) ** (252/len(cumulative_profits)) - 1, 5)
		f.write("Annualized returns based on 252 trading days per year and investing in 1 unit of iron on day 0: " +"{:.2%}\n".format(returns))
		print_dir = "long" if direction[-1] > 0 else "short"
		f.write("Direction to take now: " + print_dir)
		f.close()
		fig, ax = plt.subplots(1,2, figsize=(18,6))
		ax[0].hist(daily_profits)
		ax[0].set_title("Distribution of Daily Profits")
		ax[0].set_xlabel("Profits")
		ax[0].set_ylabel("Number of Days")
		ax[1].plot(np.arange(len(cumulative_profits)), cumulative_profits, label="Cumulative Profits")
		ax[1].plot(np.arange(len(cumulative_profits)), 
				   out_sample_price[-len(cumulative_profits):] - out_sample_price[-len(cumulative_profits)], 
				   label="Long Asset Only")
		ax[1].set_title("Cumulative Daily Profits")
		ax[1].set_xlabel("Day")
		ax[1].set_ylabel("Cumulative PNL")
		plt.legend()
		plt.savefig(fig_path)
