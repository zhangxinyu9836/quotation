


import pandas as pd
import easyquotation
import time



def task(source, datas, opt):
  #接收股票数据
  quotation = easyquotation.use(source)
  datas = pd.read_csv(datas, dtype={'codes': str})
  codes = datas['codes'].tolist()
  dict1 = quotation.stocks(codes)

  #计算收益率
  df = pd.DataFrame(dict1)
  df = df.T
  df1 = df.loc[:, ['name', 'now']]
  cost = datas['cost'].tolist()
  numbers = datas['numbers'].tolist()
  cash = datas['cash'].tolist()[0]
  df1['cost'] = cost
  df1['numbers'] = numbers
  df1['yield'] = (df1['now'] / df1['cost'] - 1).apply(lambda x: format(x, '.2'))
  total_cost = (df1['cost'] * df1['numbers']).sum() + cash
  total_capital = (df1['now'] * df1['numbers']).sum() + cash
  overall_yield1 = total_capital / total_cost - 1
  overall_yield = '%.2f%%' % (overall_yield1 * 100)

  #导出收益率结果csv
  res = pd.read_csv('res.csv')
  series = pd.Series(
    {'time': pd.datetime.now(), '股票一收益率': df1['yield'][0], '股票二收益率': df1['yield'][1], '股票三收益率': df1['yield'][2],
     '总收益率': overall_yield})
  res = res.append(series, ignore_index=True)
  print(res.head)
  res.to_csv('res.csv', index=False)

  #处理接受到的操作指令
  opt = pd.read_csv(opt, dtype={'codes': str})
  for ind in opt.index.tolist():
    ind1 = datas[datas.codes == opt.loc[ind, 'codes']].index
    datas.loc[ind1, 'numbers'] += opt.loc[ind, 'numbers']
  cash -= (opt['sell_price'] * opt['numbers']).sum()
  datas.loc[:, 'cash'] = [cash] * len(datas.index.tolist())
  datas.to_csv('datas.csv')

def run2(s,source,datas,opt):
  now = time.localtime().tm_hour + time.localtime().tm_min/60

  while 9.5 <= now <= 11.5 or 13 <= now <= 15:
    task(source,datas,opt)
    print(1)
    time.sleep(s)

def prepare(init_cash):
  #datas是股票原始状态，opt是操作指令的df，res是收益率结果df
  datas = pd.DataFrame([['300750',320,1000],['600519',1200,1000],['000002',21,150000]],columns = ['codes','cost','numbers'])
  datas.loc[:,'cash'] = [init_cash]*3
  datas.to_csv('datas.csv',index = False)

  opt = pd.DataFrame([['600519',1500,100],['000002',40,-500]], columns = ['codes','sell_price','numbers'])
  opt.to_csv('opt.csv',index = False)

  res = pd.DataFrame(columns =['time','股票一收益率','股票二收益率','股票三收益率','总收益率'])
  res.to_csv('res.csv',index=False)


def main():
  source = 'sina'
  prepare(4000000)
  s = 60
  run2(s, source, 'datas.csv', 'opt.csv')

if __name__ == '__main__':
  main()

