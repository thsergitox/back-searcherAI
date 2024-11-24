"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Checkbox } from "@/components/ui/checkbox";

const formSchema = z.object({
  prompt: z.string().min(2, {
    message: "Prompt must be at least 2 characters.",
  }),
  options: z.array(z.string()).optional(),
});

const options = [
  { id: "analytics", label: "Analytics" },
  { id: "engagement", label: "Engagement" },
  { id: "security", label: "Security" },
] as const;

export default function Home() {
  const router = useRouter();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      prompt: "",
      options: [],
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    router.push(
      `/graph?data=${encodeURIComponent(JSON.stringify(values))}`
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <Card className="p-6 shadow-lg border-gray-800 bg-gray-900">
          <h1 className="text-3xl font-bold text-center mb-6 text-gray-100 tracking-tight">
            SinergIA
          </h1>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="prompt"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-gray-200">Query</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="Enter your query..." 
                        {...field}
                        className="bg-gray-800 border-gray-700 text-gray-100"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="options"
                render={() => (
                  <FormItem>
                    <div className="mb-4">
                      <FormLabel className="text-gray-200">Options</FormLabel>
                    </div>
                    <div className="space-y-2">
                      {options.map((option) => (
                        <FormField
                          key={option.id}
                          control={form.control}
                          name="options"
                          render={({ field }) => {
                            return (
                              <FormItem
                                key={option.id}
                                className="flex flex-row items-start space-x-3 space-y-0"
                              >
                                <FormControl>
                                  <Checkbox
                                    checked={field.value?.includes(option.id)}
                                    onCheckedChange={(checked) => {
                                      return checked
                                        ? field.onChange([...(field.value || []), option.id])
                                        : field.onChange(
                                            field.value?.filter(
                                              (value) => value !== option.id
                                            )
                                          );
                                    }}
                                    className="border-gray-600"
                                  />
                                </FormControl>
                                <FormLabel className="font-normal text-gray-300">
                                  {option.label}
                                </FormLabel>
                              </FormItem>
                            );
                          }}
                        />
                      ))}
                    </div>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
                Start
              </Button>
            </form>
          </Form>
        </Card>
      </div>
    </div>
  );
}