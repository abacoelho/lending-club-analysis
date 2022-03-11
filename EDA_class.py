import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statistics import median

color_palette = ['#B3C4D6', '#30445A', '#44CFCB', '#F78E2D']
sns.set_palette(color_palette)

class EDA:
    def __init__(self, data):
        self.data = data
        
    def preliminary(self):
        """ 
        Creates boxplot of loan values and bar plot of Loans divided by term length
        """
        # Accepted loan values
        plt.figure(figsize=(8,2))
        sns.boxplot(x=self.data["loan_amnt"]/1000)
        plt.box(on=None)
        plt.title('Distribution of Accepted Loan Values', fontsize=17)
        plt.xlabel('Loan Amount (thousands)')
        plt.show()
        
        # Loans by length
        plot_df = pd.DataFrame(self.data.term.value_counts()/sum(~self.data.term.isna())*100).T
        ax = plot_df.plot.barh(stacked=True, rot=0,  figsize=(8, 2))
        plt.box(on=None)
        plt.title('Percentage of Loans by Term Length', fontsize=17)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        plt.xlabel('Percent')
        plt.yticks([], [])
        plt.show()

    def risk(self):
        """
        Creates 'risky' column in data
        Returns - Table of count and dollar value of loans by loan status       
        """
        # Risky - loans that defaulted or are over 30 days due
        self.data['risky'] = self.data.loan_status.isin(['Late (31-120 days)', 'Default'])
        
        # Loan count and value by status
        status = pd.DataFrame(self.data.loan_status.value_counts()).reset_index()
        status.columns = ['Loan Status', 'Count']
        value = pd.DataFrame(self.data.groupby(['loan_status'])['loan_amnt'].sum().reset_index())
        value.columns = ['Loan Status', 'Amount']
        status = status.merge(value, on = 'Loan Status')
        status['Count'] = status['Count'].apply(lambda x: '{:,.0f}'.format(x))
        status['Amount'] = status['Amount'].apply(lambda x: '${:,.0f}'.format(x))
        status = status.set_index('Loan Status')
        return status

    def risk_and_rates(self):
        """
        Creates box plot of distribution of loans interests by risk level     
        """
        plt.figure(figsize=(5,5))
        sns.boxplot(data = self.data, y = 'int_rate', x='risky')
        plt.box(on=None)
        plt.title('Interest Rate Distribution by Risk', fontsize=17)
        plt.xlabel('Risky')
        plt.ylabel('Interest Rate')
        plt.show()
        
    def risk_and_length(self):
        """
        Creates percentage bar plot of risk levels divided by loan length   
        """ 
        plot_df = pd.crosstab(self.data['risky'], self.data['term']).apply(lambda r: r/r.sum()*100, axis=1)
        ax = plot_df.plot.barh(stacked=True, figsize=(8,3))
        plt.box(on=None)
        plt.title('Loan Risks by Term Length', fontsize=17)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        plt.xlabel('Percent')
        plt.ylabel('Risky')
        plt.show()
        
    def risk_and_length_and_rates(self):
        """
        Creates box plot of distribution of loans interests by risk level and length   
        """         
        plt.figure(figsize=(7, 5))
        ax = sns.boxplot(data = self.data, y = 'int_rate', x='risky', hue='term')
        plt.box(on=None)
        plt.title('Interest Rate Distribution by Risk and Length', fontsize=17)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        plt.xlabel('Risky')
        plt.ylabel('Interest Rate')
        plt.show()
    
    def risk_and_grade(self):
        """
        Creates a vertical bar plot of percentage of loans at each grade divided by risk  
        """       
        plot_df = pd.crosstab(self.data['grade'], self.data['risky']).apply(lambda r: r/r.sum()*100, axis=0)
        ax = plot_df.plot.bar(figsize = (7, 5))
        plt.box(on=None)
        plt.title('Loans by Grade and Risk Level', fontsize=17)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, title = "Risky")
        plt.xlabel('Grade')
        plt.ylabel('Percent of Loans')
        plt.show()
    
    def risk_and_home_ownership(self):
        """
        Creates a bar plot of percentage of loans by home ownership divided by risk  
        """       
        plot_df = pd.crosstab(self.data['home_ownership'], self.data['risky']).apply(lambda r: r/r.sum()*100, axis=0)
        plot_df = plot_df.loc[['OWN', 'MORTGAGE', 'RENT']]
        ax = plot_df.plot.barh()
        plt.box(on=None)
        plt.title('Percentage of Loans by Home Ownership and Risk', fontsize=17)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, title = "Risky")
        plt.xlabel('Percent of Loans')
        plt.ylabel('Home Ownership')
        plt.show()
        
    def risk_and_joint_v_individual(self):
        """
        Creates a bar plot of loan risks divided by application type
        """          
        plot_df = pd.crosstab(self.data['risky'], self.data['application_type']).apply(lambda r: r/r.sum()*100, axis=1)
        ax = plot_df.plot.barh(stacked=True, figsize = (8, 3))
        plt.box(on=None)
        plt.title('Loan Risks by Application Type', fontsize=17)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        plt.xlabel('Percent')
        plt.ylabel('Risky')
        plt.show()

 
    def risk_and_verification(self):
        """
        Creates a bar plot of loan risks divided by employment verification 
        """  
        plot_df = pd.crosstab(self.data['risky'], self.data['verification_status']).apply(lambda r: r/r.sum()*100, axis=1)
        ax = plot_df.plot.barh(stacked=True, figsize = (8, 3))
        plt.box(on=None)
        plt.title('Loan Risk by Verification Status', fontsize=17)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        plt.xlabel('Percent')
        plt.ylabel('Risky')
        plt.show()
        
    def risk_and_purpose(self):
        """
        Creates a bar plot of percentage of loans by purpose divided by risk  
        """      
        plot_df = self.data[['purpose', 'risky']].sort_values('purpose')
        plot_df = pd.crosstab(plot_df['purpose'], plot_df['risky']).apply(lambda r: r/r.sum()*100, axis=0)
        ax = plot_df.plot.barh(figsize = (8, 5))
        plt.box(on=None)
        plt.title('Percentage of Loans by Purpose and Risk', fontsize=17)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], frameon=False, title = "Risky")
        plt.xlabel('Percentage of Loans')
        plt.ylabel('Loan Purpose')
        plt.show()

        
    def interest_and_FICO(self):
        """
        Creates box plots of the distribution of FICO scores by risk level 
        """  
        fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, figsize=(10, 9))
        fig.suptitle('FICO Score Distributions by Risk', fontsize=17)

        plt.subplot(221)
        ax1 = sns.boxplot(data = self.data, y = 'fico_range_low', x='risky')
        plt.box(on=None)
        plt.title('FICO Range Low')
        ax1.set_xlabel('')
        ax1.set_ylabel('')

        plt.subplot(222)
        ax2 = sns.boxplot(data = self.data, y = 'fico_range_high', x='risky')
        plt.box(on=None)
        plt.title('FICO Range High')
        ax2.set_xlabel('')
        ax2.set_ylabel('')

        plt.subplot(223)
        ax3 = sns.boxplot(data = self.data, y = 'last_fico_range_low', x='risky')
        plt.box(on=None)
        plt.title('Last FICO Range Low')
        ax3.set_xlabel('')
        ax3.set_ylabel('')

        plt.subplot(224)
        ax4 = sns.boxplot(data = self.data, y = 'last_fico_range_high', x='risky')
        plt.box(on=None)
        plt.title('Last FICO Range High')
        ax4.set_xlabel('')
        ax4.set_ylabel('')

        fig.text(0.5, 0.04, 'Risky', ha='center', fontsize = 14)
        fig.text(0.04, 0.5, 'FICO Score', va='center', rotation='vertical', fontsize = 14)
        plt.show()
        
        
        
    def interest_and_season(self):
        """
        Creates box plots of the distribution of interest rates divided by seasons  
        """          
        seasons = {'Summer':['Jun', 'Jul', 'Aug'], 
                   'Fall': ['Sep', 'Oct', 'Nov'], 
                   'Winter': ['Dec', 'Jan', 'Feb'], 
                   'Spring': ['Mar', 'Apr', 'May']}
        self.data['issue_season'] = self.data.issue_d.apply(lambda x: 
                                                                [k for k, v in seasons.items() if x[:3] in v][0])
        
        plt.figure(figsize=(7,4))
        sns.boxplot(data = self.data, x = 'int_rate', y='issue_season')
        plt.box(on=None)
        plt.title('Interest Rate Distributions by Season', fontsize=17)
        plt.xlabel('Interest Rate')
        plt.ylabel('Issue Season')
        plt.show()
