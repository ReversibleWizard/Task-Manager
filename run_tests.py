import unittest
import coverage

if __name__ == "__main__":
    cov = coverage.Coverage()
    cov.start()

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

    cov.stop()
    cov.save()
    print("\nCoverage Report:\n")
    cov.report()
    cov.html_report(directory='coverage_html')
    print("HTML version: coverage_html/index.html")