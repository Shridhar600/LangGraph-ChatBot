# -*- coding: utf-8 -*-
"""
Custom exceptions for the chatBot application.
"""

class AppException(Exception):
  """Base class for all application-specific exceptions."""
  pass

class ConfigurationError(AppException):
  """For errors related to application configuration."""
  pass

class LLMError(AppException):
  """Base for LLM related errors."""
  pass

class LLMInitializationError(LLMError):
  """For errors during LLM client initialization."""
  pass

class LLMAPIError(LLMError):
  """For errors during LLM API calls."""
  pass

class LLMToolBindError(LLMError):
  """For errors when binding tools to LLM."""
  pass

class RagError(AppException):
  """Base for RAG pipeline related errors."""
  pass

class DocumentLoadingError(RagError):
  """For errors during document loading."""
  pass

class VectorStoreError(RagError):
  """For errors related to vector store operations."""
  pass

class EmbeddingError(RagError):
  """For errors related to embedding models."""
  pass

class RagOperationError(RagError):
  """For general errors in RAG pipeline operations."""
  pass

class ToolError(AppException):
  """Base for tool related errors."""
  pass

class ToolInitializationError(ToolError):
  """For errors during tool initialization."""
  pass

class ToolExecutionError(ToolError):
  """For errors during tool execution."""
  pass

class GraphError(AppException):
  """For errors related to LangGraph execution or setup."""
  pass

class InvalidStateError(AppException):
  """For errors indicating the application is in an unexpected or invalid state."""
  pass
