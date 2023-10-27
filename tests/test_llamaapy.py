import unittest
from unittest.mock import Mock, patch
from llamaapi import LlamaAPI
import requests
import aiohttp
import asyncio

class TestLlamaAPI(unittest.TestCase):
  def setUp(self):
    self.api_token = "<your_api_token>"
    self.llama = LlamaAPI(self.api_token)

  async def run_async(self, coro):
    return await asyncio.gather(coro)

  def test_run_sync_success(self):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "Success"}

    with patch('requests.post', return_value=mock_response) as mock_post:
        # Act
        api_request_json = {"messages": [], "stream": False, "function_call": "dummy_function"}
        response = self.llama.run_sync(api_request_json)

        # Assert
        mock_post.assert_called_once_with(f"{self.llama.hostname}{self.llama.domain_path}", headers=self.llama.headers, json=api_request_json)
        self.assertEqual(response.json(), {"result": "Success"})

  def test_run_sync_failure(self):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"detail": "Internal Server Error"}

    # Act
    with patch('requests.post', return_value=mock_response):
      api_request_json = {"messages": [], "stream": False, "function_call": "dummy_function"}

      with self.assertRaises(Exception) as context:
        self.llama.run_sync(api_request_json)

    # Assert
    self.assertEqual(str(context.exception), "POST 500 Internal Server Error")

  async def test_run_stream_success(self):
    # Arrange
    mock_response = Mock()
    mock_response.status = 200
    mock_response.content.iter_any.return_value = [b'{"result": "Success"}']

    # Act
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
      api_request_json = {"messages": [], "stream": True, "function_call": "dummy_function"}

      response = await self.run_async(self.llama.run_stream(api_request_json))

    # Assert
    aiohttp.ClientSession.post.assert_called_once_with(f"{self.llama.hostname}{self.llama.domain_path}", headers=self.llama.headers, json=api_request_json)
    self.assertEqual(response, [b'{"result": "Success"}'])

  async def test_run_stream_failure(self):
    # Arrange
    mock_response = Mock()
    mock_response.status = 500
    mock_response.json.return_value = {"detail": "Internal Server Error"}

    # Act
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
      api_request_json = {"messages": [], "stream": True, "function_call": "dummy_function"}

      with self.assertRaises(Exception) as context:
        await self.run_async(self.llama.run_stream(api_request_json))

    # Assert
    self.assertEqual(str(context.exception), "POST 500 Internal Server Error")

  async def test_run_stream_for_jupyter(self):
    # Arrange
    mock_response = Mock()
    mock_response.status = 200
    mock_response.content.iter_any.return_value = [b'{"result": "Success"}']

    # Act
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
      api_request_json = {"messages": [], "stream": True, "function_call": "dummy_function"}

      await self.llama.run_stream_jupyter(api_request_json)

    # Assert
    aiohttp.ClientSession.post.assert_called_once_with(f"{self.llama.hostname}{self.llama.domain_path}", headers=self.llama.headers, json=api_request_json)

  def test_run_sync_with_non_200_response(self):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"detail": "Bad Request"}

    # Act
    with patch('requests.post', return_value=mock_response):
      api_request_json = {"messages": [], "stream": False, "function_call": "dummy_function"}

      with self.assertRaises(Exception) as context:
        self.llama.run_sync(api_request_json)

    # Assert
    self.assertEqual(str(context.exception), "POST 400 Bad Request")

  async def test_run_stream_with_non_200_response(self):
    # Arrange
    mock_response = Mock()
    mock_response.status = 400
    mock_response.json.return_value = {"detail": "Bad Request"}

    # Act
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
      api_request_json = {"messages": [], "stream": True, "function_call": "dummy_function"}

      with self.assertRaises(Exception) as context:
        await self.run_async(self.llama.run_stream(api_request_json))

    # Assert
    self.assertEqual(str(context.exception), "POST 400 Bad Request")

if __name__ == '__main__':  unittest.main()

