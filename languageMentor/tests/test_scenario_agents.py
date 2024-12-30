import unittest
from agents.scenario_agent import SalaryNegotiationAgent, RentingAgent, LeaveRequestAgent

class TestScenarioAgents(unittest.TestCase):

    def setUp(self):
        self.salary_agent = SalaryNegotiationAgent("salary_negotiation")
        self.renting_agent = RentingAgent("renting")
        self.leave_request_agent = LeaveRequestAgent("leave_request")

    def test_salary_negotiation_agent(self):
        response = self.salary_agent.chat_with_history("我想谈谈薪水")
        self.assertIn("在薪资谈判中", response)
        self.assertIn("你可以询问", response)

        response = self.salary_agent.chat_with_history("薪水")
        self.assertEqual(response, "在薪资谈判中，您可以询问：'我希望薪水能提高到多少？'")

    def test_renting_agent(self):
        response = self.renting_agent.chat_with_history("我想租房")
        self.assertIn("在租房过程中", response)
        self.assertIn("你可以询问", response)

        response = self.renting_agent.chat_with_history("租金")
        self.assertEqual(response, "在租房过程中，您可以询问：'这个房子的租金是多少？'")

    def test_leave_request_agent(self):
        response = self.leave_request_agent.chat_with_history("我需要请假")
        self.assertIn("请假时", response)
        self.assertIn("你可以说", response)

        response = self.leave_request_agent.chat_with_history("请假")
        self.assertEqual(response, "请假时，你可以说: '我需要请假几天，原因是...'")

if __name__ == '__main__':
    unittest.main() 