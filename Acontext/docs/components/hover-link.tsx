'use client';

import * as HoverCardPrimitive from '@radix-ui/react-hover-card';
import type { ComponentProps } from 'react';

export function HoverCard(props: ComponentProps<typeof HoverCardPrimitive.Root>) {
  return <HoverCardPrimitive.Root openDelay={200} closeDelay={100} {...props} />;
}

export function HoverCardTrigger({
  href,
  ...props
}: ComponentProps<'a'>) {
  return (
    <HoverCardPrimitive.Trigger asChild>
      <a href={href} {...props} />
    </HoverCardPrimitive.Trigger>
  );
}

export function HoverCardContent({
  className,
  ...props
}: ComponentProps<typeof HoverCardPrimitive.Content>) {
  return (
    <HoverCardPrimitive.Portal>
      <HoverCardPrimitive.Content
        side="top"
        sideOffset={8}
        className={[
          'z-50 w-72 rounded-xl border bg-fd-popover p-4 text-fd-popover-foreground shadow-lg',
          'animate-in fade-in-0 zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=top]:slide-in-from-bottom-2',
          className,
        ]
          .filter(Boolean)
          .join(' ')}
        {...props}
      />
    </HoverCardPrimitive.Portal>
  );
}
