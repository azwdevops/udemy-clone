import { CourseSuggest, HeroSection } from "@/components";
import Image from "next/image";

export default function Home({ data }) {
  return (
    <>
      <HeroSection />
      <CourseSuggest data={data} />
    </>
  );
}
