import  unittest,pytest
class Test_py():
    @pytest.fixture()
    def init(self):
        driver=1
        yield driver
    @pytest.mark.smoke
    @pytest.mark.usefixture("driver")
    def test_a(self,driver):
        print(driver)

if __name__ == '__main__':
    pytest.main()

