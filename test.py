import cbapi

def test_cbapi():
  try:
    cbapi.set_rapidapi_key('YOUR_RAPIDAPI_KEY')
    df_ppl = cbapi.get_people(name='Steve',types='investor', parallel=True)
    df_org = cbapi.get_organizations(name='Data', parallel=True)
  except Exception:
    print("Execution Error")

if __name__ == "__main__":
    test_cbapi()



