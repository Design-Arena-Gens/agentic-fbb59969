"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { agentsAPI } from "@/lib/api/agents";
import { ArrowLeft } from "lucide-react";
import toast from "react-hot-toast";

interface AgentFormData {
  name: string;
  framework: "crewai" | "langchain" | "openai";
  configJson: string;
}

export default function NewAgentPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<AgentFormData>();

  const onSubmit = async (data: AgentFormData) => {
    setLoading(true);
    try {
      let config: Record<string, any>;
      try {
        config = JSON.parse(data.configJson);
      } catch (e) {
        toast.error("Invalid JSON configuration");
        setLoading(false);
        return;
      }

      await agentsAPI.create({
        name: data.name,
        framework: data.framework,
        config,
      });

      toast.success("Agent created successfully!");
      router.push("/dashboard");
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to create agent");
    } finally {
      setLoading(false);
    }
  };

  const exampleConfigs = {
    crewai: `{
  "role": "Research Assistant",
  "goal": "Gather and analyze information",
  "backstory": "Expert researcher with attention to detail",
  "tools": ["search", "scrape"],
  "verbose": true
}`,
    langchain: `{
  "llm": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2000,
  "tools": ["calculator", "wikipedia"],
  "memory": "conversation_buffer"
}`,
    openai: `{
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 1500,
  "system_message": "You are a helpful assistant"
}`,
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center">
            <button
              onClick={() => router.back()}
              className="inline-flex items-center text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="h-5 w-5 mr-2" />
              Back
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">
              Create New Agent
            </h1>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Agent Name
                </label>
                <input
                  type="text"
                  {...register("name", {
                    required: "Agent name is required",
                  })}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="My Research Agent"
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.name.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Framework
                </label>
                <select
                  {...register("framework", {
                    required: "Framework is required",
                  })}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  onChange={(e) => {
                    const framework = e.target.value as keyof typeof exampleConfigs;
                    const textarea = document.getElementById(
                      "configJson"
                    ) as HTMLTextAreaElement;
                    if (textarea && exampleConfigs[framework]) {
                      textarea.value = exampleConfigs[framework];
                    }
                  }}
                >
                  <option value="">Select a framework</option>
                  <option value="crewai">CrewAI</option>
                  <option value="langchain">Langchain</option>
                  <option value="openai">OpenAI</option>
                </select>
                {errors.framework && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.framework.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Configuration (JSON)
                </label>
                <textarea
                  id="configJson"
                  {...register("configJson", {
                    required: "Configuration is required",
                  })}
                  rows={12}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 font-mono text-sm"
                  placeholder='{\n  "key": "value"\n}'
                />
                {errors.configJson && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.configJson.message}
                  </p>
                )}
                <p className="mt-2 text-sm text-gray-500">
                  Select a framework to load an example configuration
                </p>
              </div>

              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => router.back()}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                >
                  {loading ? "Creating..." : "Create Agent"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
